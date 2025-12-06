
"""
Patient class for the Hospital Management System
"""

from datetime import datetime
from typing import Dict
from person import Person


class Patient(Person):
    """Patient class with medical information"""
    
    def __init__(self, patient_id: int, name: str, age: int, gender: str, 
                 contact: str, disease: str):
        super().__init__(patient_id, name, age, gender, contact)
        self._disease = disease
        self._admission_date = datetime.now().strftime("%Y-%m-%d")
    
    @property
    def disease(self):
        return self._disease
    
    @disease.setter
    def disease(self, value):
        self._disease = value
    
    @property
    def admission_date(self):
        return self._admission_date
    
    def display_info(self) -> str:
        """Display complete patient information"""
        base_info = super().display_info()
        return f"{base_info}, Disease: {self._disease}, Admitted: {self._admission_date}"
    
    def to_dict(self) -> Dict:
        """Convert patient object to dictionary for JSON serialization"""
        return {
            'patient_id': self._person_id,
            'name': self._name,
            'age': self._age,
            'gender': self._gender,
            'contact': self._contact,
            'disease': self._disease,
            'admission_date': self._admission_date
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Patient':
        """Create patient object from dictionary"""
        patient = Patient(
            data['patient_id'],
            data['name'],
            data['age'],
            data['gender'],
            data['contact'],
            data['disease']
        )
        patient._admission_date = data.get('admission_date', 
                                          datetime.now().strftime("%Y-%m-%d"))
        return patient