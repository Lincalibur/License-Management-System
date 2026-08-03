from tkinter import messagebox

import customtkinter as ctk

from license_management_backend import GoogleCredentialsMissingError, notify_expiring_licenses
from license_management_db import add_license, create_tables, export_licenses_csv


class LicenseManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("License Management System")
        self.geometry("400x420")

        create_tables()

        ctk.CTkLabel(self, text="License Name").pack(pady=(15, 0))
        self.entry_name = ctk.CTkEntry(self)
        self.entry_name.pack(pady=5)

        ctk.CTkLabel(self, text="License Key").pack(pady=(10, 0))
        self.entry_key = ctk.CTkEntry(self)
        self.entry_key.pack(pady=5)

        ctk.CTkLabel(self, text="Expiration Date (YYYY-MM-DD)").pack(pady=(10, 0))
        self.entry_expiration_date = ctk.CTkEntry(self)
        self.entry_expiration_date.pack(pady=5)

        ctk.CTkLabel(self, text="Notification Email").pack(pady=(10, 0))
        self.entry_email = ctk.CTkEntry(self)
        self.entry_email.pack(pady=5)

        ctk.CTkButton(self, text="Add License", command=self.add_license_gui).pack(pady=10)
        ctk.CTkButton(self, text="Export CSV Report", command=self.export_report).pack(pady=5)
        ctk.CTkButton(self, text="Send Expiry Notifications", command=self.send_notifications).pack(pady=5)

    def add_license_gui(self):
        name = self.entry_name.get()
        key = self.entry_key.get()
        expiration_date = self.entry_expiration_date.get()
        email = self.entry_email.get()

        result = add_license(name, key, expiration_date, email)

        if result != "OK":
            messagebox.showerror("Error", result)
            return

        messagebox.showinfo("Success", f"License '{name}' added successfully.")
        self.entry_name.delete(0, "end")
        self.entry_key.delete(0, "end")
        self.entry_expiration_date.delete(0, "end")
        self.entry_email.delete(0, "end")

    def export_report(self):
        path = export_licenses_csv()
        messagebox.showinfo("Report Generated", f"License report written to:\n{path}")

    def send_notifications(self):
        try:
            notify_expiring_licenses(30)
            messagebox.showinfo("Notifications Sent", "Expiry notification emails have been sent.")
        except GoogleCredentialsMissingError as e:
            messagebox.showerror("Google credentials missing", str(e))


def main():
    app = LicenseManagerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
