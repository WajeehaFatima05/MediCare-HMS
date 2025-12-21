
import tkinter as tk
from tkinter import ttk, messagebox
from hospital_system import HospitalSystem

class MediCareGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MediCare Hospital Management System")
        self.root.geometry("1200x850")
        
        # Initialize backend logic
        self.system = HospitalSystem()
        
        # --- UI Theme (Figma Blue & White) ---
        self.COLOR_PRIMARY = "#0056b3"   
        self.COLOR_BG = "#f8f9fa"        
        self.COLOR_WHITE = "#ffffff"
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TNotebook", background=self.COLOR_BG, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.COLOR_PRIMARY, foreground="white", padding=[15, 5])
        self.style.map("TNotebook.Tab", background=[("selected", self.COLOR_WHITE)], foreground=[("selected", self.COLOR_PRIMARY)])

        self.root.configure(bg=self.COLOR_BG)
        self.setup_ui()

    def setup_ui(self):
        # Header Section
        header = tk.Frame(self.root, bg=self.COLOR_PRIMARY, height=80)
        header.pack(fill="x")
        tk.Label(header, text="🏥 MediCare HMS Suite", font=("Helvetica", 24, "bold"), 
                 bg=self.COLOR_PRIMARY, fg="white").pack(pady=15)

        # Tabbed Navigation
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)

        # Define Frames
        self.tab_dash = tk.Frame(self.tabs, bg=self.COLOR_WHITE)
        self.tab_patients = tk.Frame(self.tabs, bg=self.COLOR_WHITE)
        self.tab_doctors = tk.Frame(self.tabs, bg=self.COLOR_WHITE)
        self.tab_appts = tk.Frame(self.tabs, bg=self.COLOR_WHITE)
        self.tab_billing = tk.Frame(self.tabs, bg=self.COLOR_WHITE)

        self.tabs.add(self.tab_dash, text=" Dashboard ")
        self.tabs.add(self.tab_patients, text=" Patients ")
        self.tabs.add(self.tab_doctors, text=" Doctors ")
        self.tabs.add(self.tab_appts, text=" Appointments ")
        self.tabs.add(self.tab_billing, text=" Billing ")

        # Initialize All Logic Modules
        self.init_dashboard()
        self.init_patient_tab()
        self.init_doctor_tab()
        self.init_appointment_tab()
        self.init_billing_tab()

    # ==================== 1. DOCTOR MANAGEMENT ====================
    def init_doctor_tab(self):
        f = tk.LabelFrame(self.tab_doctors, text=" Register New Doctor ", bg=self.COLOR_WHITE, padx=10, pady=10)
        f.pack(fill="x", padx=20, pady=10)

        self.d_name = self.create_input(f, "Name:", 0, 0)
        self.d_spec = self.create_input(f, "Specialty:", 0, 2)
        self.d_avail = self.create_input(f, "Availability (Days):", 0, 4)

        tk.Button(f, text="Add Doctor", command=self.add_doctor_logic, bg="#28a745", fg="white", width=15).grid(row=1, column=5, pady=10)

        self.d_tree = self.create_tree(self.tab_doctors, ("ID", "Name", "Specialty", "Availability"))
        self.refresh_d_list()

    def add_doctor_logic(self):
        try:
            name = self.d_name.get()
            spec = self.d_spec.get()
            avail = self.d_avail.get()
            if name and spec:
                # Assuming standard placeholder values for age, gender, contact not in form
                self.system.add_doctor(name, 35, "N/A", "N/A", spec, avail)
                messagebox.showinfo("Success", f"Doctor {name} added!")
                self.refresh_all()
            else:
                messagebox.showwarning("Input Error", "Name and Specialty are required.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==================== 2. APPOINTMENT SCHEDULING ====================
    def init_appointment_tab(self):
        f = tk.LabelFrame(self.tab_appts, text=" Schedule Appointment ", bg=self.COLOR_WHITE, padx=10, pady=10)
        f.pack(fill="x", padx=20, pady=10)

        self.a_pid = self.create_input(f, "Patient ID:", 0, 0)
        self.a_did = self.create_input(f, "Doctor ID:", 0, 2)
        self.a_date = self.create_input(f, "Date (YYYY-MM-DD):", 1, 0)
        self.a_time = self.create_input(f, "Time (HH:MM):", 1, 2)

        tk.Button(f, text="Book Appointment", command=self.add_appt_logic, bg=self.COLOR_PRIMARY, fg="white", width=20).grid(row=1, column=4, padx=10)

        self.a_tree = self.create_tree(self.tab_appts, ("Appt ID", "Patient ID", "Doctor ID", "Date", "Time", "Status"))
        self.refresh_a_list()

    def add_appt_logic(self):
        try:
            p_id = int(self.a_pid.get())
            d_id = int(self.a_did.get())
            date = self.a_date.get()
            time = self.a_time.get()
            
            self.system.schedule_appointment(p_id, d_id, date, time)
            messagebox.showinfo("Success", "Appointment Scheduled!")
            self.refresh_all()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid Numeric IDs.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==================== 3. DATA REFRESH LOGIC ====================
    def refresh_all(self):
        """Updates all tables and dashboard stats at once"""
        self.update_stats()
        self.refresh_p_list()
        self.refresh_d_list()
        self.refresh_a_list()
        self.refresh_b_list()

    def refresh_a_list(self):
        for i in self.a_tree.get_children(): self.a_tree.delete(i)
        for a in self.system._appointments: # Accessing internal list from hospital_system
            self.a_tree.insert("", "end", values=(a.appointment_id, a.patient_id, a.doctor_id, a.date, a.time, a.status))

    # ==================== HELPER METHODS ====================
    def create_input(self, parent, label, r, c):
        tk.Label(parent, text=label, bg=self.COLOR_WHITE, font=("Helvetica", 10)).grid(row=r, column=c, padx=5, pady=8, sticky="e")
        ent = ttk.Entry(parent, width=18)
        ent.grid(row=r, column=c+1, padx=5, pady=8)
        return ent

    def create_tree(self, parent, cols):
        container = tk.Frame(parent, bg=self.COLOR_WHITE)
        container.pack(fill="both", expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(container, columns=cols, show='headings', height=12)
        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        return tree

    # (Previous Patient, Billing, and Dashboard methods remain same but call self.refresh_all())
    def init_dashboard(self):
        tk.Label(self.tab_dash, text="MediCare Analytics Dashboard", font=("Helvetica", 20, "bold"), bg=self.COLOR_WHITE, fg=self.COLOR_PRIMARY).pack(pady=30)
        self.stats_label = tk.Label(self.tab_dash, text="", font=("Courier New", 14), bg="#eef6ff", padx=50, pady=40, relief="groove", bd=2)
        self.stats_label.pack(pady=10)
        tk.Button(self.tab_dash, text="🔄 Sync System Data", bg=self.COLOR_PRIMARY, fg="white", font=("Helvetica", 10, "bold"), command=self.refresh_all, padx=20).pack(pady=20)
        self.update_stats()

    def update_stats(self):
        s = self.system.get_statistics()
        text = (f"📈 PATIENTS REGISTERED:  {s['total_patients']}\n"
                f"👨‍⚕️ ACTIVE DOCTORS:      {s['total_doctors']}\n"
                f"📅 APPOINTMENTS:        {s['scheduled_appointments']}\n"
                f"💳 PENDING INVOICES:    {s['total_bills'] - s['paid_bills']}\n"
                f"--------------------------------------\n"
                f"💰 TOTAL REVENUE:       ${s['total_revenue']:.2f}")
        self.stats_label.config(text=text)

    def init_patient_tab(self):
        f = tk.LabelFrame(self.tab_patients, text=" Patient Intake Form ", bg=self.COLOR_WHITE, padx=10, pady=10)
        f.pack(fill="x", padx=20, pady=10)
        self.p_name = self.create_input(f, "Name:", 0, 0)
        self.p_age = self.create_input(f, "Age:", 0, 2)
        self.p_gen = self.create_input(f, "Gender:", 0, 4)
        self.p_con = self.create_input(f, "Contact:", 1, 0)
        self.p_dis = self.create_input(f, "Disease:", 1, 2)
        tk.Button(f, text="Register", command=self.add_patient_logic, bg="#28a745", fg="white", width=12).grid(row=1, column=5)
        self.p_tree = self.create_tree(self.tab_patients, ("ID", "Name", "Age", "Gender", "Disease", "Date"))
        self.refresh_p_list()

    def add_patient_logic(self):
        try:
            self.system.add_patient(self.p_name.get(), int(self.p_age.get()), self.p_gen.get(), self.p_con.get(), self.p_dis.get())
            messagebox.showinfo("MediCare", "Patient Record Added Successfully")
            self.refresh_all()
        except: messagebox.showerror("Input Error", "Invalid data in form fields.")

    def init_billing_tab(self):
        f = tk.LabelFrame(self.tab_billing, text=" Financial Entry ", bg=self.COLOR_WHITE, padx=10, pady=10)
        f.pack(fill="x", padx=20, pady=10)
        self.b_pid = self.create_input(f, "Patient ID:", 0, 0)
        self.b_con = self.create_input(f, "Consultation:", 0, 2)
        self.b_med = self.create_input(f, "Medication:", 0, 4)
        tk.Button(f, text="Generate Bill", command=self.billing_logic, bg=self.COLOR_PRIMARY, fg="white").grid(row=0, column=6, padx=10)
        self.b_tree = self.create_tree(self.tab_billing, ("Bill ID", "Patient ID", "Date", "Total", "Status"))
        tk.Button(self.tab_billing, text="✔ Mark Selected as Paid", command=self.pay_bill_logic, bg="#17a2b8", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
        self.refresh_b_list()

    def billing_logic(self):
        try:
            self.system.generate_bill(int(self.b_pid.get()), float(self.b_con.get()), float(self.b_med.get()))
            self.refresh_all()
        except: messagebox.showerror("Billing Error", "Check Patient ID and fee amounts.")

    def pay_bill_logic(self):
        selected = self.b_tree.selection()
        if selected:
            bid = self.b_tree.item(selected[0])['values'][0]
            if self.system.mark_bill_as_paid(bid):
                messagebox.showinfo("Billing", "Payment confirmed.")
                self.refresh_all()

    def refresh_p_list(self):
        for i in self.p_tree.get_children(): self.p_tree.delete(i)
        for p in self.system._patients:
            self.p_tree.insert("", "end", values=(p.person_id, p.name, p.age, p.gender, p.disease, p.admission_date))

    def refresh_d_list(self):
        for i in self.d_tree.get_children(): self.d_tree.delete(i)
        for d in self.system._doctors:
            self.d_tree.insert("", "end", values=(d.person_id, d.name, d.specialization, d.availability))

    def refresh_b_list(self):
        for i in self.b_tree.get_children(): self.b_tree.delete(i)
        for b in self.system._bills:
            self.b_tree.insert("", "end", values=(b.bill_id, b.patient_id, b.date, f"${b.total}", b.payment_status))

if __name__ == "__main__":
    root = tk.Tk()
    app = MediCareGUI(root)
    root.mainloop()