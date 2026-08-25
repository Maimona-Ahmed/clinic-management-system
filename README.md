# Clinic Management System — Backend

A backend REST API for a Clinic Management System, built with Django and Django REST Framework.

The system provides APIs for managing users, doctors, patients, services, appointments, medical records, invoices, and payments.

## 🚀 Technologies

* Python
* Django
* Django REST Framework
* Simple JWT
* SQLite
* Django ORM
* RESTful APIs

## 📁 Project Structure

```text
backend/
│
├── accounts/
├── doctors/
├── patients/
├── services/
├── appointments/
├── medical_records/
├── payments/
│
├── manage.py
├── requirements.txt
├── db.sqlite3
└── README.md
```

## 🔐 Authentication

The system uses JWT authentication with access and refresh tokens.

Authentication APIs include:

* User Registration
* Login
* Token Refresh
* Logout
* Current User Profile
* Change Password
* Forgot Password
* Reset Password

## 👨‍⚕️ Doctors

Doctor management APIs include:

* Doctor profiles
* Doctor services
* Doctor schedules
* Doctor time off
* Doctor availability
* Consultation fees

## 🧑‍🤝‍🧑 Patients

Patient APIs provide management of:

* Patient profiles
* Patient information
* Patient appointments
* Patient medical records

## 🏥 Services

The system provides APIs for managing clinic services and their availability for doctors.

Examples:

* General Consultation
* ECG
* Other medical services

## 📅 Appointments

The appointment system supports:

* Creating appointments
* Viewing appointments
* Appointment ownership
* Doctor schedules
* Working hours validation
* Doctor time-off validation
* Doctor slot conflict prevention
* Patient appointment conflict prevention
* Appointment cancellation
* Appointment status management

Appointment flow:

```text
PENDING
   │
   ▼
CONFIRMED
   │
   ▼
COMPLETED
```

Appointments can also be cancelled when allowed by the business rules.

## 🩺 Medical Records

Medical record APIs support clinical information associated with appointments and patients.

The medical system includes:

* Consultations
* Medical records
* Prescriptions
* Clinical information

## 💳 Payments

The payment system is connected directly to appointments.

Flow:

```text
Appointment
     │
     ▼
Confirmed Appointment
     │
     ▼
Invoice
     │
     ├── UNPAID
     │
     ├── PAID
     │
     └── CANCELLED
          │
          ▼
       Payment
```

Payment functionality includes:

* Invoice creation
* Invoice viewing
* Invoice cancellation
* Payment creation
* Payment tracking
* Payment status management
* Remaining invoice amount calculation

Supported payment methods:

```text
CASH
CARD
BANK_TRANSFER
```

## 🌐 API Structure

The main API groups are:

```text
/api/auth/
/api/doctors/
/api/patients/
/api/services/
/api/appointments/
/api/medical-records/
/api/payments/
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/clinic-management.git
```

### 2. Enter the backend directory

```bash
cd clinic-management/backend
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## 🔑 Admin Panel

Django Admin is available at:

```text
http://127.0.0.1:8000/admin/
```

The admin panel can be used to manage system data and administrative operations.

## 🧪 Testing

The project includes API tests covering important business rules and permissions.

Run the tests with:

```bash
python manage.py test
```

## 📌 Database

The project currently uses SQLite for development.

```text
SQLite
└── db.sqlite3
```

The database file is excluded from version control.

## 📄 License

This project was developed for educational and portfolio purposes.
