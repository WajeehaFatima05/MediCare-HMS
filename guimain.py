import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from hospital_system import HospitalSystem

class MediCareGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MediCare Hospital Management System")
        self.root.geometry("1200x800")
        
        # Initialize backend
        self.system = HospitalSystem()
        
        # --- Color Palette ---
        self.COLOR_PRIMARY = "#0056b3"   # Medical Blue
        self.COLOR_BG = "#f8f9fa"        # Off-White
        self.COLOR_WHITE = "#ffffff"
        
        # --- Styles ---
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TNotebook", background=self.COLOR_BG, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.COLOR_PRIMARY, foreground=self.COLOR_WHITE, 
                            padding=[15, 5], font=('Helvetica', 10, 'bold'))
        self.style.map("TNotebook.Tab", background=[("selected", self.COLOR_WHITE)], 
                      foreground=[("selected", self.COLOR_PRIMARY)])
        
        self.root.configure(bg=self.COLOR_BG)
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.COLOR_PRIMARY, height=80)
        header.pack(fill="x")
        tk.Label(header, text="🏥 MediCare HMS", font=("Helvetica", 26, "bold"), 
                 bg=self.COLOR_PRIMARY, fg=self.COLOR_WHITE).pack(pady=15)

        # Tab Control
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=20)

        # Create Tabs
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

        self.init_dashboard()
        self.init_patient_tab()
        self.init_doctor_tab()
        self.init_appointment_tab()
        self.init_billing_tab()

    # ==================== DASHBOARD ====================
    def init_dashboard(self):
        tk.Label(self.tab_dash, text="Hospital Performance Overview", font=("Helvetica", 18, "bold"), 
                 bg=self.COLOR_WHITE, fg=self.COLOR_PRIMARY).pack(pady=30)
        
        self.stats_label = tk.Label(self.tab_dash, text="", font=("Courier", 14), 
                                   bg="#eef6ff", padx=40, pady=40, relief="solid", bd=1)
        self.stats_label.pack(pady=10)
        
        tk.Button(self.tab_dash, text="Refresh Data", bg=self.COLOR_PRIMARY, fg="white", 
                  command=self.refresh_all).pack(pady=20)
        self.update_stats()

    def update_stats(self):
        s = self.system.get_statistics()
        text = (f"Total Patients:      {s['total_patients']}\n"
                f"Total Doctors:       {s['total_doctors']}\n"
                f"Active Appointments: {s['scheduled_appointments']}\n"
                f"Total Invoices:      {s['total_bills']}\n"
                f"-------------------------------\n"
                f"Total Revenue:       ${s['total_revenue']:.2f}")
        self.stats_label.config(text=text)

    # ==================== PATIENTS ====================
    def init_patient_tab(self):
        f = tk.LabelFrame(self.tab_patients, text=" Register Patient ", bg=self.COLOR_WHITE, padx=10, pady=10)
        f.pack(fill="x", padx=20, pady=10)
        
        self.p_name = self.create_input(f, "Name:", 0, 0)
        self.p_age = self.create_input(f, "Age:", 0, 2)
        self.p_gen = self.create_input(f, "Gender:", 0, 4)
        self.p_con = self.create_input(f, "Contact:", 1, 0)
        self.p_dis = self.create_input(f, "Disease:", 1, 2)

        tk.Button(f, text="Add Patient", command=self.add_patient_logic, bg="#28a745", fg="white").grid(row=1, column=5, padx=10)

        self.p_tree = self.create_tree(self.tab_patients, ("ID", "Name", "Age", "Gender", "Disease", "Admitted"))
        
        self.p_menu = tk.Menu(self.root, tearoff=0)
        self.p_menu.add_command(label="Update Disease", command=self.update_patient_ui)
        self.p_menu.add_separator()
        self.p_menu.add_command(label="Delete Patient", command=self.delete_patient_logic, foreground="red")
        
        self.p_tree.bind("<Button-3>", lambda e: self.p_menu.post(e.x_root, e.y_root))
        self.refresh_p_list()

    def add_patient_logic(self):
        try:
            self.system.add_patient(self.p_name.get(), int(self.p_age.get()), self.p_gen.get(), 
                                    self.p_con.get(), self.p_dis.get())
            messagebox.showinfo("Success", "Patient Registered")
            self.refresh_all()
        except: messagebox.showerror("Error", "Check Inputs")

    def update_patient_ui(self):
        selected = self.p_tree.selection()
        if not selected: return
        p_id = self.p_tree.item(selected[0])['values'][0]
        new_dis = simpledialog.askstring("Update", "Enter new disease:")
        if new_dis:
            for p in self.system._patients:
                if p.person_id == p_id:
                    p.disease = new_dis
                    self.system.save_data()
                    self.refresh_all()

    def delete_patient_logic(self):
        selected = self.p_tree.selection()
        if not selected: return
        p_id = self.p_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Delete Patient?"):
            self.system._patients = [p for p in self.system._patients if p.person_id != p_id]
            self.system.save_data()
            self.refresh_all()

    # ==================== DOCTORS (NEW FUNCTIONALITY) ====================
    def init_doctor_tab(self):
        # Form to Add Doctor
        f = tk.LabelFrame(self.tab_doctors, text=" Register Doctor ", bg=self.COLOR_WHITE, padx=10, pady=10)
        f.pack(fill="x", padx=20, pady=10)
        
        self.d_name = self.create_input(f, "Name:", 0, 0)
        self.d_age = self.create_input(f, "Age:", 0, 2)
        self.d_spec = self.create_input(f, "Specialty:", 0, 4)
        self.d_con = self.create_input(f, "Contact:", 1, 0)
        self.d_avail = self.create_input(f, "Availability:", 1, 2)

        tk.Button(f, text="Add Doctor", command=self.add_doctor_logic, bg="#28a745", fg="white").grid(row=1, column=5, padx=10)

        # Table
        self.d_tree = self.create_tree(self.tab_doctors, ("ID", "Name", "Specialty", "Availability", "Contact"))
        
        # Menu for Update/Delete
        self.d_menu = tk.Menu(self.root, tearoff=0)
        self.d_menu.add_command(label="Update Availability", command=self.update_doctor_ui)
        self.d_menu.add_separator()
        self.d_menu.add_command(label="Delete Doctor", command=self.delete_doctor_logic, foreground="red")
        
        self.d_tree.bind("<Button-3>", lambda e: self.d_menu.post(e.x_root, e.y_root))
        self.refresh_d_list()

    def add_doctor_logic(self):
        try:
            # Note: Ensure your hospital_system.py has an add_doctor method
            self.system.add_doctor(self.d_name.get(), int(self.d_age.get()), "M/F", 
                                   self.d_con.get(), self.d_spec.get(), self.d_avail.get())
            messagebox.showinfo("Success", "Doctor Registered")
            self.refresh_all()
        except: messagebox.showerror("Error", "Check Inputs")

    def update_doctor_ui(self):
        selected = self.d_tree.selection()
        if not selected: return
        d_id = self.d_tree.item(selected[0])['values'][0]
        new_avail = simpledialog.askstring("Update", "Enter new availability (e.g. Mon-Fri):")
        if new_avail:
            for d in self.system._doctors:
                if d.person_id == d_id:
                    d._availability = new_avail # Accessing private member for quick update
                    self.system.save_data()
                    self.refresh_all()

    def delete_doctor_logic(self):
        selected = self.d_tree.selection()
        if not selected: return
        d_id = self.d_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Delete Doctor?"):
            self.system._doctors = [d for d in self.system._doctors if d.person_id != d_id]
            self.system.save_data()
            self.refresh_all()

    # ==================== APPOINTMENTS ====================
    def init_appointment_tab(self):
        f = tk.LabelFrame(self.tab_appts, text=" Schedule Appointment ", bg=self.COLOR_WHITE, padx=10, pady=10)
        f.pack(fill="x", padx=20, pady=10)
        self.a_pid = self.create_input(f, "Patient ID:", 0, 0)
        self.a_did = self.create_input(f, "Doctor ID:", 0, 2)
        self.a_date = self.create_input(f, "Date:", 0, 4)
        tk.Button(f, text="Book", command=self.book_appt_logic, bg=self.COLOR_PRIMARY, fg="white").grid(row=0, column=6, padx=10)

        self.a_tree = self.create_tree(self.tab_appts, ("Appt ID", "Pat ID", "Doc ID", "Date", "Status"))
        self.refresh_a_list()

    def book_appt_logic(self):
        try:
            self.system.schedule_appointment(int(self.a_pid.get()), int(self.a_did.get()), self.a_date.get(), "10:00 AM")
            self.refresh_all()
        except: messagebox.showerror("Error", "Check IDs")

    # ==================== BILLING ====================
    def init_billing_tab(self):
        f = tk.LabelFrame(self.tab_billing, text=" Generate Bill ", bg=self.COLOR_WHITE, padx=10, pady=10)
        f.pack(fill="x", padx=20, pady=10)
        self.b_pid = self.create_input(f, "Patient ID:", 0, 0)
        self.b_con = self.create_input(f, "Consult Fee:", 0, 2)
        self.b_med = self.create_input(f, "Meds Fee:", 0, 4)
        tk.Button(f, text="Invoice", command=self.billing_logic, bg=self.COLOR_PRIMARY, fg="white").grid(row=0, column=6, padx=10)

        self.b_tree = self.create_tree(self.tab_billing, ("Bill ID", "Pat ID", "Date", "Total", "Status"))
        tk.Button(self.tab_billing, text="Mark Paid", command=self.pay_bill_logic, bg="#17a2b8", fg="white").pack(pady=5)
        self.refresh_b_list()

    def billing_logic(self):
        try:
            self.system.generate_bill(int(self.b_pid.get()), float(self.b_con.get()), float(self.b_med.get()))
            self.refresh_all()
        except: messagebox.showerror("Error", "Invalid Input")

    def pay_bill_logic(self):
        selected = self.b_tree.selection()
        if selected:
            bid = self.b_tree.item(selected[0])['values'][0]
            self.system.mark_bill_as_paid(bid)
            self.refresh_all()

    # ==================== HELPERS & REFRESH ====================
    def create_input(self, parent, label, r, c):
        tk.Label(parent, text=label, bg=self.COLOR_WHITE).grid(row=r, column=c, padx=5, pady=5, sticky="e")
        ent = ttk.Entry(parent, width=15)
        ent.grid(row=r, column=c+1, padx=5, pady=5)
        return ent

    def create_tree(self, parent, cols):
        tree = ttk.Treeview(parent, columns=cols, show='headings')
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        tree.pack(fill="both", expand=True, padx=20, pady=10)
        return tree

    def refresh_all(self):
        self.update_stats()
        self.refresh_p_list()
        self.refresh_d_list()
        self.refresh_a_list()
        self.refresh_b_list()

    def refresh_p_list(self):
        for i in self.p_tree.get_children(): self.p_tree.delete(i)
        for p in self.system.get_all_patients():
            self.p_tree.insert("", "end", values=(p.person_id, p.name, p.age, p.gender, p.disease, p.admission_date))

    def refresh_d_list(self):
        for i in self.d_tree.get_children(): self.d_tree.delete(i)
        for d in self.system.get_all_doctors():
            self.d_tree.insert("", "end", values=(d.person_id, d.name, d.specialization, d.availability, d.contact))

    def refresh_a_list(self):
        for i in self.a_tree.get_children(): self.a_tree.delete(i)
        for a in self.system._appointments:
            self.a_tree.insert("", "end", values=(a.appointment_id, a.patient_id, a.doctor_id, a.date, a.status))

    def refresh_b_list(self):
        for i in self.b_tree.get_children(): self.b_tree.delete(i)
        for b in self.system.get_all_bills():
            self.b_tree.insert("", "end", values=(b.bill_id, b.patient_id, b.date, f"${b.total}", b.payment_status))

if __name__ == "__main__":
    root = tk.Tk()
    app = MediCareGUI(root)
    root.mainloop()