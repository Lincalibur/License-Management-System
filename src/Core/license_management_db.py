import sqlite3

def create_connection():
    conn = sqlite3.connect('license_management.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Create licenses table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS licenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        key TEXT NOT NULL,
                        expiration_date TEXT NOT NULL,
                        email TEXT NOT NULL)''')
    
    conn.commit()
    conn.close()

def add_license(name, key, expiration_date, email):
    if not name or not key or not expiration_date or not email:
        return "Invalid input. Please fill out all fields."
    
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO licenses (name, key, expiration_date, email) VALUES (?, ?, ?, ?)",
                   (name, key, expiration_date, email))
    
    conn.commit()
    conn.close()

def fetch_all_licenses():
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM licenses")
    licenses = cursor.fetchall()
    
    conn.close()
    return licenses

def get_license_by_id(license_id):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM licenses WHERE id=?", (license_id,))
    license = cursor.fetchone()
    
    conn.close()
    return license
