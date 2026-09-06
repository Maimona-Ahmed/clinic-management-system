# 🏥 Clinic Management System

A full-stack clinic management system designed to manage patients, doctors, appointments, medical records, consultations, and prescriptions.

## 🚀 Technologies

### Backend

* Python
* Django
* Django REST Framework

### Frontend

* React
* JavaScript
* HTML
* CSS

## ✨ Features

* 🔐 Authentication & Authorization
* 👨‍⚕️ Doctor Management
* 🧑‍⚕️ Patient Management
* 📅 Appointment Management
* 🩺 Consultation Management
* 📋 Medical Records
* 💊 Prescription Management
* 🔌 RESTful APIs


## 🏗️ Project Structure

```text
clinic-management/
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md
```

## ⚙️ Backend Setup

### 1. Navigate to the backend

```bash
cd backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file inside the `backend` directory.

Use `.env.example` as a reference.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the backend server

```bash
python manage.py runserver
```

The backend will run at:

```text
http://127.0.0.1:8000/
```

## 🎨 Frontend Setup

### 1. Navigate to the frontend

```bash
cd frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Start the development server

```bash
npm run dev
```

## 🔌 API

The backend provides RESTful APIs for:

* Authentication
* Doctors
* Patients
* Appointments
* Medical Records
* Consultations
* Prescriptions




## 🔐 Security

Sensitive configuration such as:

* Django `SECRET_KEY`
* Database credentials
* Other environment-specific settings

are stored in environment variables and should not be committed to the repository.

## 🧪 Testing

Backend tests can be run using:

```bash
python manage.py test
```

## 📌 Project Status

🚧 This project is currently under development.

## 👨‍💻 Authors

Developed as a full-stack software project using Django and React.

## 📄 License

This project is for educational and development purposes.
