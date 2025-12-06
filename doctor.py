
"""
Doctor class for the Hospital Management System
"""

from typing import Dict
from person import Person


class Doctor(Person):
    """Doctor class with specialization and availability"""
    
    def __init__(self, doctor_id: int, name: str, age: int, gender: str, 
                 contact: str, specialization: str, availability: str):
        super().__init__(doctor_id, name, age, gender, contact)
        self._specialization = specialization
        self._availability = availability
    
    @property
    def specialization(self):
        return self._specialization
    
    @property
    def availability(self):
        return self._availability
    
    def check_availability(self, day: str) -> bool:
        """Check if doctor is available on given day"""
        return day.lower() in self._availability.lower()
    
    def display_info(self) -> str:
        """Display complete doctor information"""
        base_info = super().display_info()
        return (f"{base_info}, Specialization: {self._specialization}, "
                f"Available: {self._availability}")
    
    def to_dict(self) -> Dict:
        """Convert doctor object to dictionary for JSON serialization"""
        return {
            'doctor_id': self._person_id,
            'name': self._name,
            'age': self._age,
            'gender': self._gender,
            'contact': self._contact,
            'specialization': self._specialization,
            'availability': self._availability
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Doctor':
        """Create doctor object from dictionary"""
        return Doctor(
            data['doctor_id'],
            data['name'],
            data['age'],
            data['gender'],
            data['contact'],
            data['specialization'],
            data['availability']
        )
    
