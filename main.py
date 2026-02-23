from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path as PathLib
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Optional

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# creating pydantic model for patient
class Patient(BaseModel):
    id: Annotated[str ,Field(..., description='Unique identifier for the patient' , example = 'P001')]
    name: Annotated[str, Field(..., description='Full name of the patient' , example = 'John Doe')]
    city: Annotated[str , Field(..., description='City where the patient resides' , example = 'New York')]
    age: Annotated[int , Field(..., description='Age of the patient in years' , example = 30)]
    gender: Annotated[str , Field(..., description='Gender of the patient' , example = 'Male')]
    height: Annotated[float,Field(...,gt =0, description='Height of the patient in centimeters' , example = 175.5)]
    weight: Annotated[float , Field(...,gt =0, description='Weight of the patient in kilograms' , example = 70.2)]


#computed field to calculate bmi
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    @computed_field
    @property
    def verdict(self)-> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= self.bmi < 24.9:
            return 'Normal weight'
        elif 25 <= self.bmi < 29.9:
            return 'Overweight'
        else:
            return 'Obesity'
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default =None)]
    city: Annotated[Optional[str] , Field(default =None )]
    age: Annotated[Optional[int] , Field(default =None)]
    gender: Annotated[Optional[str] , Field(default =None)]
    height: Annotated[Optional[float],Field(default =None,gt =0 )]
    weight: Annotated[Optional[float] , Field(default=None,gt =0)]     
#helper function
def load_data():
    with open('patients.json' ,'r') as f:
        data = json.load(f)
    return data
def save_data(data):
    with open('patients.json' , 'w') as f:
        json.dump(data , f)    


@app.get("/")
def serve_frontend():
    """Serve the interactive frontend"""
    return FileResponse(PathLib(__file__).parent / "static" / "index.html")
@app.get("/about")
def about():
    return {"About": "A fully functional patient management system to manage patient records."}
@app.get("/view")
def view():
    data = load_data()
    return data
@app.get("/patient/{patient_id}")
def view_patient(patient_id:str = Path(..., description= 'ID of the patient in the DB ' , example = 'P001')):
    data = load_data()
    
    if patient_id in data :
        return data[patient_id]
    raise HTTPException(status_code =404 , detail = 'Patient not found')
# endpoint to sort patients by age height anbmi
# give option to sort in ascending or descending order    
@app.get("/sort")
def sort_partients(sort_by: str = Query(..., description = 'sort of the basis of height , weight or BMI'), order: str = Query('asc', description = 'Order of sorting - asc or desc ')):

   valid_fields = ['weight' , 'height' , 'bmi']
   if sort_by not in valid_fields:
       raise HTTPException(status_code = 400 , detail = f'Invalid sort field. Valid fields are {valid_fields}')
   if order not in ['asc','desc']:
       raise HTTPException(status_code = 400 , detail = 'Invalid order. Valid orders are asc and desc')
   data = load_data()
   reverse = True if order == 'desc' else False
   sorted_data = sorted(data.values() , key = lambda x: x[sort_by] , reverse = reverse)
   return sorted_data


# post endpoint to add new patient
@app.post('/create')
def create_patient(patient:Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code = 400 , detail = 'Patient with this ID already exists')
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(content={"message": "Patient created successfully"}, status_code=201)


# put endpoint to update patient details
@app.put('/edit/{patient_id}')
def update_patient(patient_id:str , patient_update:PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code = 404 , detail = 'Patient not found')
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')
    data[patient_id] = existing_patient_info
    save_data(data)
    return JSONResponse(content={"message": "Patient updated successfully"}, status_code=200)
    
   
# delete endpoint to delete patient
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'})

