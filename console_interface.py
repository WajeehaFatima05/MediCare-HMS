
from hospital_system import HospitalSystem


class ConsoleInterface:
    """Console-based user interface"""
    
    def __init__(self):
        self.hospital = HospitalSystem()
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("        MediCare Hospital Management System")
        print("="*50)
        print("1. Patient Management")
        print("2. Doctor Management")
        print("3. Appointment Management")
        print("4. Billing Management")
        print("5. Reports & Statistics")
        print("6. Exit")
        print("="*50)
    
    # ==================== PATIENT MENU ====================
    
    def patient_menu(self):
        """Patient management submenu"""
        while True:
            print("\n--- Patient Management ---")
            print("1. Add Patient")
            print("2. View All Patients")
            print("3. Search Patient by ID")
            print("4. Search Patient by Name")
            print("5. Update Patient")
            print("6. Delete Patient")
            print("7. Back to Main Menu")
            
            choice = input("\nEnter choice: ")
            
            if choice == '1':
                self.add_patient()
            elif choice == '2':
                self.view_patients()
            elif choice == '3':
                self.search_patient_by_id()
            elif choice == '4':
                self.search_patient_by_name()
            elif choice == '5':
                self.update_patient()
            elif choice == '6':
                self.delete_patient()
            elif choice == '7':
                break
            else:
                print("❌ Invalid choice!")
    
    def add_patient(self):
        """Add a new patient"""
        print("\n--- Add New Patient ---")
        try:
            name = input("Name: ").strip()
            age = int(input("Age: "))
            gender = input("Gender (M/F/Other): ").strip()
            contact = input("Contact: ").strip()
            disease = input("Disease: ").strip()
            
            if age < 0 or age > 150:
                print("❌ Invalid age!")
                return
            
            patient = self.hospital.add_patient(name, age, gender, contact, disease)
            print(f"\n✅ Patient added successfully! ID: {patient.person_id}")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def view_patients(self):
        """View all patients"""
        print("\n--- All Patients ---")
        patients = self.hospital.get_all_patients()
        if not patients:
            print("No patients found.")
            return
        
        for patient in patients:
            print(patient.display_info())
    
    def search_patient_by_id(self):
        """Search patient by ID"""
        try:
            patient_id = int(input("\nEnter Patient ID: "))
            patient = self.hospital.get_patient(patient_id)
            if patient:
                print("\n" + patient.display_info())
            else:
                print("❌ Patient not found.")
        except ValueError:
            print("❌ Invalid ID")
    
    def search_patient_by_name(self):
        """Search patients by name"""
        name = input("\nEnter patient name: ").strip()
        patients = self.hospital.search_patient_by_name(name)
        if patients:
            print(f"\n--- Found {len(patients)} patient(s) ---")
            for patient in patients:
                print(patient.display_info())
        else:
            print("❌ No patients found with that name.")
    
    def update_patient(self):
        """Update patient information"""
        try:
            patient_id = int(input("\nEnter Patient ID: "))
            patient = self.hospital.get_patient(patient_id)
            if not patient:
                print("❌ Patient not found.")
                return
            
            print(f"\nCurrent disease: {patient.disease}")
            disease = input("New Disease: ").strip()
            
            if self.hospital.update_patient(patient_id, disease=disease):
                print("✅ Patient updated successfully!")
            else:
                print("❌ Update failed.")
        except ValueError:
            print("❌ Invalid input")
    
    def delete_patient(self):
        """Delete a patient"""
        try:
            patient_id = int(input("\nEnter Patient ID to delete: "))
            patient = self.hospital.get_patient(patient_id)
            if not patient:
                print("❌ Patient not found.")
                return
            
            print(f"\nPatient: {patient.name}")
            confirm = input("Are you sure? (yes/no): ").lower()
            
            if confirm == 'yes':
                if self.hospital.delete_patient(patient_id):
                    print("✅ Patient deleted successfully!")
                else:
                    print("❌ Deletion failed.")
        except ValueError:
            print("❌ Invalid ID")
    
    # ==================== DOCTOR MENU ====================
    
    def doctor_menu(self):
        """Doctor management submenu"""
        while True:
            print("\n--- Doctor Management ---")
            print("1. Add Doctor")
            print("2. View All Doctors")
            print("3. Search Doctor by ID")
            print("4. Search Doctor by Specialization")
            print("5. Delete Doctor")
            print("6. Back to Main Menu")
            
            choice = input("\nEnter choice: ")
            
            if choice == '1':
                self.add_doctor()
            elif choice == '2':
                self.view_doctors()
            elif choice == '3':
                self.search_doctor_by_id()
            elif choice == '4':
                self.search_doctor_by_specialization()
            elif choice == '5':
                self.delete_doctor()
            elif choice == '6':
                break
            else:
                print("❌ Invalid choice!")
    
    def add_doctor(self):
        """Add a new doctor"""
        print("\n--- Add New Doctor ---")
        try:
            name = input("Name: ").strip()
            age = int(input("Age: "))
            gender = input("Gender (M/F/Other): ").strip()
            contact = input("Contact: ").strip()
            specialization = input("Specialization: ").strip()
            availability = input("Availability (e.g., Mon-Fri 9-5): ").strip()
            
            if age < 0 or age > 150:
                print("❌ Invalid age!")
                return
            
            doctor = self.hospital.add_doctor(name, age, gender, contact, 
                                             specialization, availability)
            print(f"\n✅ Doctor added successfully! ID: {doctor.person_id}")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def view_doctors(self):
        """View all doctors"""
        print("\n--- All Doctors ---")
        doctors = self.hospital.get_all_doctors()
        if not doctors:
            print("No doctors found.")
            return
        
        for doctor in doctors:
            print(doctor.display_info())
    
    def search_doctor_by_id(self):
        """Search doctor by ID"""
        try:
            doctor_id = int(input("\nEnter Doctor ID: "))
            doctor = self.hospital.get_doctor(doctor_id)
            if doctor:
                print("\n" + doctor.display_info())
            else:
                print("❌ Doctor not found.")
        except ValueError:
            print("❌ Invalid ID")
    
    def search_doctor_by_specialization(self):
        """Search doctors by specialization"""
        specialization = input("\nEnter specialization: ").strip()
        doctors = self.hospital.search_doctor_by_specialization(specialization)
        if doctors:
            print(f"\n--- Found {len(doctors)} doctor(s) ---")
            for doctor in doctors:
                print(doctor.display_info())
        else:
            print("❌ No doctors found with that specialization.")
    
    def delete_doctor(self):
        """Delete a doctor"""
        try:
            doctor_id = int(input("\nEnter Doctor ID to delete: "))
            doctor = self.hospital.get_doctor(doctor_id)
            if not doctor:
                print("❌ Doctor not found.")
                return
            
            print(f"\nDoctor: {doctor.name}")
            confirm = input("Are you sure? (yes/no): ").lower()
            
            if confirm == 'yes':
                if self.hospital.delete_doctor(doctor_id):
                    print("✅ Doctor deleted successfully!")
                else:
                    print("❌ Deletion failed.")
        except ValueError:
            print("❌ Invalid ID")
    
    # ==================== APPOINTMENT MENU ====================
    
    def appointment_menu(self):
        """Appointment management submenu"""
        while True:
            print("\n--- Appointment Management ---")
            print("1. Schedule Appointment")
            print("2. View All Appointments")
            print("3. View Patient Appointments")
            print("4. View Doctor Appointments")
            print("5. Cancel Appointment")
            print("6. Back to Main Menu")
            
            choice = input("\nEnter choice: ")
            
            if choice == '1':
                self.schedule_appointment()
            elif choice == '2':
                self.view_appointments()
            elif choice == '3':
                self.view_patient_appointments()
            elif choice == '4':
                self.view_doctor_appointments()
            elif choice == '5':
                self.cancel_appointment()
            elif choice == '6':
                break
            else:
                print("❌ Invalid choice!")
    
    def schedule_appointment(self):
        """Schedule a new appointment"""
        print("\n--- Schedule Appointment ---")
        try:
            patient_id = int(input("Patient ID: "))
            doctor_id = int(input("Doctor ID: "))
            date = input("Date (DD-MM-YYYY): ").strip()
            time = input("Time (HH:MM): ").strip()
            
            appointment = self.hospital.schedule_appointment(patient_id, doctor_id, 
                                                            date, time)
            print(f"\n✅ Appointment scheduled! ID: {appointment.appointment_id}")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
  


    def view_all_appointments(self):
      print("\n--- All Appointments ---")
      appointments = self.hospital.get_all_appointments()
      if not appointments:
            print("No appointments found.")
            return
        
      for appt in appointments:
            print(appt.display_details())
    
    def view_patient_appointments(self):
        """View appointments for a specific patient"""
        try:
            patient_id = int(input("\nEnter Patient ID: "))
            appointments = self.hospital.get_patient_appointments(patient_id)
            if appointments:
                print(f"\n--- Appointments for Patient {patient_id} ---")
                for appt in appointments:
                    print(appt.display_details())
            else:
                print("❌ No appointments found for this patient.")
        except ValueError:
            print("❌ Invalid ID")
    
    def view_doctor_appointments(self):
        """View appointments for a specific doctor"""
        try:
            doctor_id = int(input("\nEnter Doctor ID: "))
            appointments = self.hospital.get_doctor_appointments(doctor_id)
            if appointments:
                print(f"\n--- Appointments for Doctor {doctor_id} ---")
                for appt in appointments:
                    print(appt.display_details())
            else:
                print("❌ No appointments found for this doctor.")
        except ValueError:
            print("❌ Invalid ID")
    
    def cancel_appointment(self):
        """Cancel an appointment"""
        try:
            appt_id = int(input("\nEnter Appointment ID to cancel: "))
            appointment = self.hospital.get_appointment(appt_id)
            if not appointment:
                print("❌ Appointment not found.")
                return
            
            print(f"\n{appointment.display_details()}")
            confirm = input("Cancel this appointment? (yes/no): ").lower()
            
            if confirm == 'yes':
                if self.hospital.cancel_appointment(appt_id):
                    print("✅ Appointment cancelled successfully!")
                else:
                    print("❌ Cancellation failed.")
        except ValueError:
            print("❌ Invalid ID")
    
    # ==================== BILLING MENU ====================
    
    def billing_menu(self):
        """Billing management submenu"""
        while True:
            print("\n--- Billing Management ---")
            print("1. Generate Bill")
            print("2. View All Bills")
            print("3. View Patient Bills")
            print("4. Mark Bill as Paid")
            print("5. Back to Main Menu")
            
            choice = input("\nEnter choice: ")
            
            if choice == '1':
                self.generate_bill()
            elif choice == '2':
                self.view_bills()
            elif choice == '3':
                self.view_patient_bills()
            elif choice == '4':
                self.mark_bill_paid()
            elif choice == '5':
                break
            else:
                print("❌ Invalid choice!")
    
    def generate_bill(self):
        """Generate a new bill"""
        print("\n--- Generate Bill ---")
        try:
            patient_id = int(input("Patient ID: "))
            consultation_fee = float(input("Consultation Fee: $"))
            medication_fee = float(input("Medication Fee: $"))
            
            bill = self.hospital.generate_bill(patient_id, consultation_fee, 
                                              medication_fee)
            print("\n✅ Bill Generated!")
            print(bill.display_bill())
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def view_bills(self):
        """View all bills"""
        print("\n--- All Bills ---")
        bills = self.hospital.get_all_bills()
        if not bills:
            print("No bills found.")
            return
        
        for bill in bills:
            print(bill.display_bill())
    
    def view_patient_bills(self):
        """View bills for a specific patient"""
        try:
            patient_id = int(input("\nEnter Patient ID: "))
            bills = self.hospital.get_patient_bills(patient_id)
            if not bills:
                print("❌ No bills found for this patient.")
                return
            
            print(f"\n--- Bills for Patient {patient_id} ---")
            for bill in bills:
                print(bill.display_bill())
        except ValueError:
            print("❌ Invalid ID")
    
    def mark_bill_paid(self):
        """Mark a bill as paid"""
        try:
            bill_id = int(input("\nEnter Bill ID: "))
            if self.hospital.mark_bill_paid(bill_id):
                print("✅ Bill marked as paid!")
            else:
                print("❌ Bill not found.")
        except ValueError:
            print("❌ Invalid ID")
    
    # ==================== REPORTS ====================
    
    def reports_menu(self):
        """Display system statistics and reports"""
        print("\n" + "="*50)
        print("           SYSTEM STATISTICS")
        print("="*50)
        
        stats = self.hospital.get_statistics()
        
        print(f"\n📊 Patient Information:")
        print(f"   Total Patients: {stats['total_patients']}")
        
        print(f"\n👨‍⚕️ Doctor Information:")
        print(f"   Total Doctors: {stats['total_doctors']}")
        
        print(f"\n📅 Appointment Information:")
        print(f"   Total Appointments: {stats['total_appointments']}")
        print(f"   Scheduled: {stats['scheduled_appointments']}")
        
        print(f"\n💰 Financial Information:")
        print(f"   Total Bills: {stats['total_bills']}")
        print(f"   Paid Bills: {stats['paid_bills']}")
        print(f"   Total Revenue: ${stats['total_revenue']:.2f}")
        
        print("\n" + "="*50)
        input("\nPress Enter to continue...")
    
    # ==================== MAIN LOOP ====================
    
    def run(self):
        """Main program loop"""
        print("\n🏥 Welcome to MediCare Hospital Management System!")
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.patient_menu()
            elif choice == '2':
                self.doctor_menu()
            elif choice == '3':
                self.appointment_menu()
            elif choice == '4':
                self.billing_menu()
            elif choice == '5':
                self.reports_menu()
            elif choice == '6':
                print("\n✅ Thank you for using MediCare HMS!")
                print("🏥 System shutting down...")
                break
            else:
                print("❌ Invalid choice! Please try again.")