import customtkinter as ctk
from license_management_backend import notify_expiring_licenses
from license_management_db import add_license, create_tables

app = ctk.CTk()
app.title("License Management System")
app.geometry("400x300")

# Initialize the database
create_tables()

def add_license_gui():
    name = entry_name.get()
    key = entry_key.get()
    expiration_date = entry_expiration_date.get()
    email = entry_email.get()
    
    result = add_license(name, key, expiration_date, email)
    
    if result == "Invalid input. Please fill out all fields.":
        ctk.CTkMessagebox.showinfo("Error", result)
    else:
        ctk.CTkMessagebox.showinfo("Success", f"License '{name}' added successfully.")

def export_report():
    notify_expiring_licenses(30)
    ctk.CTkMessagebox.showinfo("Report Generated", "The license report has been generated.")

# GUI Elements
label_name = ctk.CTkLabel(app, text="License Name")
label_name.pack(pady=10)
entry_name = ctk.CTkEntry(app)
entry_name.pack(pady=5)

label_key = ctk.CTkLabel(app, text="License Key")
label_key.pack(pady=10)
entry_key = ctk.CTkEntry(app)
entry_key.pack(pady=5)

label_expiration_date = ctk.CTkLabel(app, text="Expiration Date (YYYY-MM-DD)")
label_expiration_date.pack(pady=10)
entry_expiration_date = ctk.CTkEntry(app)
entry_expiration_date.pack(pady=5)

label_email = ctk.CTkLabel(app, text="Email")
label_email.pack(pady=10)
entry_email = ctk.CTkEntry(app)
entry_email.pack(pady=5)

add_button = ctk.CTkButton(app, text="Add License", command=add_license_gui)
add_button.pack(pady=10)

report_button = ctk.CTkButton(app, text="Export Report", command=export_report)
report_button.pack(pady=10)

app.mainloop()
