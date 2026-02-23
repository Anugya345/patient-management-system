🏥 Patient Management System API (FastAPI)

A lightweight and fully functional Patient Management System built using FastAPI, featuring patient creation, update, delete, sorting, and automatic BMI & health verdict calculation.

This project is perfect for learning FastAPI, Pydantic models, JSON-based storage, CRUD operations, and computed fields.

🚀 Features

✨ Create patient records

✨ Update patient details

✨ Delete a patient

✨ View all patients

✨ View a single patient by ID

✨ Sort patients by:

Height

Weight

BMI

✨ Automatic BMI calculation using computed fields

✨ Automatic health verdict based on BMI

✨ JSON-file-based database (no external DB)

✨ Fully documented API with Swagger UI

🧠 Tech Stack

FastAPI

Python 3.10+

Pydantic

JSON Storage

Uvicorn

📂 Project Structure
patient-api/
│
├── main.py               # Main FastAPI application
├── patients.json         # JSON file storing patient records
├── README.md             # Documentation
└── requirements.txt      # Python dependencies

📦 Installation
1. Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

2. Install dependencies
pip install -r requirements.txt

3. Run the server
uvicorn main:app --reload

🌐 API Documentation (Auto-generated)

Once server starts, open:

Swagger UI:

http://127.0.0.1:8000/docs


ReDoc:

http://127.0.0.1:8000/redoc

📝 API Endpoints
✔ GET /

Welcome message

✔ GET /about

Project description

✔ GET /view

Return entire patient database

✔ GET /patient/{patient_id}

Fetch a single patient by ID

✔ GET /sort?sort_by=height&order=asc

Sort by height, weight, or BMI

✔ POST /create

Create a new patient

BMI & verdict auto-calculated

✔ PUT /edit/{patient_id}

Update an existing patient

✔ DELETE /delete/{patient_id}

Delete a patient

🧮 BMI & Verdict Logic

BMI Formula:

BMI = weight / (height * height)


Verdict rules:

BMI < 18.5 → Underweight

18.5 – 24.9 → Normal

25 – 29.9 → Overweight

= 30 → Obesity

📘 Sample JSON Record
{
  "P001": {
    "name": "John Doe",
    "city": "Delhi",
    "age": 30,
    "gender": "Male",
    "height": 1.75,
    "weight": 70,
    "bmi": 22.86,
    "verdict": "Normal weight"
  }
}

🔧 Future Improvements

Add authentication (JWT)

Add proper database (MongoDB / PostgreSQL)

Add pagination

Add search by city / name

Add filtering (age, gender)

Add frontend using React

🤝 Contributing

Pull requests are welcome! Open an issue to discuss major changes.