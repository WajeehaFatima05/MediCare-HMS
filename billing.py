
"""
Billing class for the Hospital Management System
"""

from datetime import datetime
from typing import Dict


class Billing:
    """Billing class for managing patient charges"""
    
    def __init__(self, bill_id: int, patient_id: int, consultation_fee: float, 
                 medication_fee: float):
        self._bill_id = bill_id
        self._patient_id = patient_id
        self._consultation_fee = consultation_fee
        self._medication_fee = medication_fee
        self._total = self.calculate_total()
        self._date = datetime.now().strftime("%Y-%m-%d %H:%M")
        self._payment_status = "Unpaid"
    
    @property
    def bill_id(self):
        return self._bill_id
    
    @property
    def patient_id(self):
        return self._patient_id
    
    @property
    def total(self):
        return self._total
    
    @property
    def payment_status(self):
        return self._payment_status
    
    def calculate_total(self) -> float:
        """Calculate total bill amount"""
        return self._consultation_fee + self._medication_fee
    
    def mark_as_paid(self):
        """Mark bill as paid"""
        self._payment_status = "Paid"
    
    def display_bill(self) -> str:
        """Display formatted bill"""
        return (f"\n{'='*40}\n"
                f"           BILL RECEIPT\n"
                f"{'='*40}\n"
                f"Bill ID: {self._bill_id}\n"
                f"Patient ID: {self._patient_id}\n"
                f"Date: {self._date}\n"
                f"{'-'*40}\n"
                f"Consultation Fee: ${self._consultation_fee:.2f}\n"
                f"Medication Fee:   ${self._medication_fee:.2f}\n"
                f"{'-'*40}\n"
                f"Total Amount:     ${self._total:.2f}\n"
                f"Payment Status:   {self._payment_status}\n"
                f"{'='*40}")
    
    def to_dict(self) -> Dict:
        """Convert billing object to dictionary"""
        return {
            'bill_id': self._bill_id,
            'patient_id': self._patient_id,
            'consultation_fee': self._consultation_fee,
            'medication_fee': self._medication_fee,
            'total': self._total,
            'date': self._date,
            'payment_status': self._payment_status
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Billing':
        """Create billing object from dictionary"""
        billing = Billing(
            data['bill_id'],
            data['patient_id'],
            data['consultation_fee'],
            data['medication_fee']
        )
        billing._date = data.get('date', datetime.now().strftime("%Y-%m-%d %H:%M"))
        billing._payment_status = data.get('payment_status', 'Unpaid')
        return billing
    
