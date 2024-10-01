import customtkinter as ctk
from license_management_backend import add_license, get_all_licenses, generate_report, notify_expiring_licenses

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("License Management System")

def add_license_gui():
    name = name_entry.get()
    key = key_entry.get()
    expiration_date = expiration_entry.get()
    
    add_license(name, key, expiration_date)
    name_entry.delete(0, ctk.END)
    key_entry.delete(0, ctk.END)
    expiration_entry.delete(0, ctk.END)
    update_license_list()

def update_license_list():
    for widget in license_list_frame.winfo_children():
        widget.destroy()
        
    licenses = get_all_licenses()
    for lic in licenses:
        ctk.CTkLabel(license_list_frame, text=f"ID: {lic[0]}, Name: {lic[1]}, Key: {lic[2]}, Expiration: {lic[3]}").pack()

def export_report():
    generate_report()
    ctk.CTkMessagebox.showinfo("Report Generated", "The license report has been generated as 'license_report.csv'.")

# Create GUI elements
name_entry = ctk.CTkEntry(app, placeholder_text="License Name")
name_entry.pack(pady=10)

key_entry = ctk.CTkEntry(app, placeholder_text="License Key")
key_entry.pack(pady=10)

expiration_entry = ctk.CTkEntry(app, placeholder_text="Expiration Date (YYYY-MM-DD)")
expiration_entry.pack(pady=10)

add_button = ctk.CTkButton(app, text="Add License", command=add_license_gui)
add_button.pack(pady=10)

license_list_frame = ctk.CTkFrame(app)
license_list_frame.pack(pady=10)

export_button = ctk.CTkButton(app, text="Generate License Report", command=export_report)
export_button.pack(pady=20)

notify_expiring_licenses(30, "recipient_email@example.com")  # Change to the user's email
update_license_list()

app.mainloop()
