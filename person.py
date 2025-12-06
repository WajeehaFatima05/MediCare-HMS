
"""
Base Person class for the Hospital Management System
"""

class Person:
    """Base class for all persons in the system"""
    
    def __init__(self, person_id: int, name: str, age: int, gender: str, contact: str):
        self._person_id = person_id
        self._name = name
        self._age = age
        self._gender = gender
        self._contact = contact
    
    @property
    def person_id(self):
        return self._person_id
    
    @property
    def name(self):
        return self._name
    
    @property
    def age(self):
        return self._age
    
    @property
    def gender(self):
        return self._gender
    
    @property
    def contact(self):
        return self._contact
    
    def display_info(self) -> str:
        """Display basic person information"""
        return (f"ID: {self._person_id}, Name: {self._name}, "
                f"Age: {self._age}, Gender: {self._gender}, "
                f"Contact: {self._contact}")