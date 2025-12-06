
"""
Appointment class for the Hospital Management System
"""

from typing import Dict


class Appointment:
    """Appointment class for scheduling patient-doctor meetings"""
    
    def __init__(self, appointment_id: int, patient_id: int, doctor_id: int, 
                 date: str, time: str):
        self._appointment_id = appointment_id
        self._patient_id = patient_id
        self._doctor_id = doctor_id
        self._date = date
        self._time = time
        self._status = "Scheduled"
    
    @property
    def appointment_id(self):
        return self._appointment_id
    
    @property
    def patient_id(self):
        return self._patient_id
    
    @property
    def doctor_id(self):
        return self._doctor_id
    
    @property
    def status(self):
        return self._status
    
    def cancel_appointment(self):
        """Cancel the appointment"""
        self._status = "Cancelled"
    
    def complete_appointment(self):
        """Mark appointment as completed"""
        self._status = "Completed"
    
    def reschedule(self, new_date: str, new_time: str):
        """Reschedule the appointment"""
        self._date = new_date
        self._time = new_time
        self._status = "Rescheduled"
    
    def display_details(self) -> str:
        """Display appointment details"""
        return (f"Appointment ID: {self._appointment_id}, "
                f"Patient ID: {self._patient_id}, "
                f"Doctor ID: {self._doctor_id}, "
                f"Date: {self._date}, Time: {self._time}, "
                f"Status: {self._status}")
    
    def to_dict(self) -> Dict:
        """Convert appointment object to dictionary"""
        return {
            'appointment_id': self._appointment_id,
            'patient_id': self._patient_id,
            'doctor_id': self._doctor_id,
            'date': self._date,
            'time': self._time,
            'status': self._status
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Appointment':
        """Create appointment object from dictionary"""
        appointment = Appointment(
            data['appointment_id'],
            data['patient_id'],
            data['doctor_id'],
            data['date'],
            data['time']
        )
        appointment._status = data.get('status', 'Scheduled')
        return appointment
