
#  MediCare Hospital Management System

A comprehensive Object-Oriented Hospital Management System built with Python.

##  Features

- **Patient Management**: Add, view, update, and delete patient records
- **Doctor Management**: Manage doctor information and specializations
- **Appointment Scheduling**: Book and manage patient-doctor appointments
- **Billing System**: Generate and track patient bills with payment status
- **Reports & Statistics**: View comprehensive system analytics

## How to Run
```bash
python main.py
```

## 📦 Requirements

- Python 3.7 or higher
- No external libraries required (uses only Python standard library)

## Project Structure
```
MediCare_HMS/
├── person.py              # Base Person class
├── patient.py             # Patient class with medical info
├── doctor.py              # Doctor class with specialization
├── appointment.py         # Appointment scheduling
├── billing.py             # Billing and payment management
├── hospital_system.py     # Main system logic
├── console_interface.py   # Console user interface
└── main.py                # Entry point
```

## OOP Concepts Implemented

-  **Encapsulation**: Private attributes with property decorators
-  **Inheritance**: Person base class extended by Patient and Doctor
-  **Polymorphism**: Overridden display methods
-  **Abstraction**: Clean, modular interfaces
-  **Data Persistence**: JSON-based storage system

##  Data Storage

All data is automatically saved to `hospital_data.json` file and persists between sessions.



