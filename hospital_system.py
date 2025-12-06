

"""
Main Hospital System class - Central management system
"""

import json
import os
from typing import List, Optional

from patient import Patient
from doctor import Doctor
from appointment import Appointment
from billing import Billing


class HospitalSystem:
    """Main hospital management system coordinating all modules"""
    
    def __init__(self, data_file: str = "hospital_data.json"):
        self._patients: List[Patient] = []
        self._doctors: List[Doctor] = []
        self._appointments: List[Appointment] = []
        self._bills: List[Billing] = []
        self._data_file = data_file
        self.load_data()
    
    # ==================== PATIENT MANAGEMENT ====================
    
    def add_patient(self, name: str, age: int, gender: str, contact: str, 
                   disease: str) -> Patient:
        """Add a new patient to the system"""
        patient_id = len(self._patients) + 1
        patient = Patient(patient_id, name, age, gender, contact, disease)
        self._patients.append(patient)
        self.save_data()
        return patient
    
    def get_patient(self, patient_id: int) -> Optional[Patient]:
        """Get patient by ID"""
        for patient in self._patients:
            if patient.person_id == patient_id:
                return patient
        return None
    
    def get_all_patients(self) -> List[Patient]:
        """Get all patients"""
        return self._patients
    
    def update_patient(self, patient_id: int, **kwargs) -> bool:
        """Update patient information"""
        patient = self.get_patient(patient_id)
        if patient:
            if 'disease' in kwargs:
                patient.disease = kwargs['disease']
            self.save_data()
            return True
        return False
    
    def delete_patient(self, patient_id: int) -> bool:
        """Delete a patient"""
        patient = self.get_patient(patient_id)
        if patient:
            self._patients.remove(patient)
            self.save_data()
            return True
        return False
    
    def search_patient_by_name(self, name: str) -> List[Patient]:
        """Search patients by name"""
        return [p for p in self._patients if name.lower() in p.name.lower()]
    
    # ==================== DOCTOR MANAGEMENT ====================
    
    def add_doctor(self, name: str, age: int, gender: str, contact: str, 
                  specialization: str, availability: str) -> Doctor:
        """Add a new doctor to the system"""
        doctor_id = len(self._doctors) + 1
        doctor = Doctor(doctor_id, name, age, gender, contact, 
                       specialization, availability)
        self._doctors.append(doctor)
        self.save_data()
        return doctor
    
    def get_doctor(self, doctor_id: int) -> Optional[Doctor]:
        """Get doctor by ID"""
        for doctor in self._doctors:
            if doctor.person_id == doctor_id:
                return doctor
        return None
    
    def get_all_doctors(self) -> List[Doctor]:
        """Get all doctors"""
        return self._doctors
    
    def delete_doctor(self, doctor_id: int) -> bool:
        """Delete a doctor"""
        doctor = self.get_doctor(doctor_id)
        if doctor:
            self._doctors.remove(doctor)
            self.save_data()
            return True
        return False
    
    def search_doctor_by_specialization(self, specialization: str) -> List[Doctor]:
        """Search doctors by specialization"""
        return [d for d in self._doctors 
                if specialization.lower() in d.specialization.lower()]
    
    # ==================== APPOINTMENT MANAGEMENT ====================
    
    def schedule_appointment(self, patient_id: int, doctor_id: int, 
                           date: str, time: str) -> Optional[Appointment]:
        """Schedule a new appointment"""
        if not self.get_patient(patient_id):
            raise ValueError("Patient not found")
        if not self.get_doctor(doctor_id):
            raise ValueError("Doctor not found")
        
        # Check for conflicts
        for appt in self._appointments:
            if (appt.doctor_id == doctor_id and appt._date == date and 
                appt._time == time and appt.status == "Scheduled"):
                raise ValueError("Time slot already booked for this doctor")
        
        appointment_id = len(self._appointments) + 1
        appointment = Appointment(appointment_id, patient_id, doctor_id, date, time)
        self._appointments.append(appointment)
        self.save_data()
        return appointment
    
    def get_appointment(self, appointment_id: int) -> Optional[Appointment]:
        """Get appointment by ID"""
        for appt in self._appointments:
            if appt.appointment_id == appointment_id:
                return appt
        return None
    
    def get_all_appointments(self) -> List[Appointment]:
        """Get all appointments"""
        return self._appointments
    
    def cancel_appointment(self, appointment_id: int) -> bool:
        """Cancel an appointment"""
        appointment = self.get_appointment(appointment_id)
        if appointment:
            appointment.cancel_appointment()
            self.save_data()
            return True
        return False
    
    def get_patient_appointments(self, patient_id: int) -> List[Appointment]:
        """Get all appointments for a patient"""
        return [a for a in self._appointments if a.patient_id == patient_id]
    
    def get_doctor_appointments(self, doctor_id: int) -> List[Appointment]:
        """Get all appointments for a doctor"""
        return [a for a in self._appointments if a.doctor_id == doctor_id]
    
    # ==================== BILLING MANAGEMENT ====================
    
    def generate_bill(self, patient_id: int, consultation_fee: float, 
                     medication_fee: float) -> Optional[Billing]:
        """Generate a new bill"""
        if not self.get_patient(patient_id):
            raise ValueError("Patient not found")
        
        if consultation_fee < 0 or medication_fee < 0:
            raise ValueError("Fees cannot be negative")
        
        bill_id = len(self._bills) + 1
        bill = Billing(bill_id, patient_id, consultation_fee, medication_fee)
        self._bills.append(bill)
        self.save_data()
        return bill
    
    def get_bill(self, bill_id: int) -> Optional[Billing]:
        """Get bill by ID"""
        for bill in self._bills:
            if bill.bill_id == bill_id:
                return bill
        return None
    
    def get_all_bills(self) -> List[Billing]:
        """Get all bills"""
        return self._bills
    
    def get_patient_bills(self, patient_id: int) -> List[Billing]:
        """Get all bills for a patient"""
        return [bill for bill in self._bills if bill.patient_id == patient_id]
    
    def mark_bill_paid(self, bill_id: int) -> bool:
        """Mark a bill as paid"""
        bill = self.get_bill(bill_id)
        if bill:
            bill.mark_as_paid()
            self.save_data()
            return True
        return False
    
    # ==================== DATA PERSISTENCE ====================
    
    def save_data(self):
        """Save all data to JSON file"""
        data = {
            'patients': [p.to_dict() for p in self._patients],
            'doctors': [d.to_dict() for d in self._doctors],
            'appointments': [a.to_dict() for a in self._appointments],
            'bills': [b.to_dict() for b in self._bills]
        }
        try:
            with open(self._data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        """Load all data from JSON file"""
        if os.path.exists(self._data_file):
            try:
                with open(self._data_file, 'r') as f:
                    data = json.load(f)
                
                self._patients = [Patient.from_dict(p) 
                                 for p in data.get('patients', [])]
                self._doctors = [Doctor.from_dict(d) 
                                for d in data.get('doctors', [])]
                self._appointments = [Appointment.from_dict(a) 
                                     for a in data.get('appointments', [])]
                self._bills = [Billing.from_dict(b) 
                              for b in data.get('bills', [])]
            except Exception as e:
                print(f"Error loading data: {e}")
    
    # ==================== STATISTICS ====================
    
    def get_statistics(self) -> dict:
        """Get system statistics"""
        total_revenue = sum(bill.total for bill in self._bills)
        paid_bills = sum(1 for bill in self._bills 
                        if bill.payment_status == "Paid")
        
        return {
            'total_patients': len(self._patients),
            'total_doctors': len(self._doctors),
            'total_appointments': len(self._appointments),
            'scheduled_appointments': sum(1 for a in self._appointments 
                                         if a.status == "Scheduled"),
            'total_bills': len(self._bills),
            'paid_bills': paid_bills,
            'total_revenue': total_revenue
        }
    