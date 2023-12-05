import sqlite3
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

conn = sqlite3.connect('password_manager.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()


def encrypt_data(data):
    return cipher_suite.encrypt(data.encode())


def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data).decode()


def add_password():
    service = input("Enter the service name: ")
    username = input("Enter the username: ")
    password = input("Enter the password: ")

    encrypted_password = encrypt_data(password)

    cursor.execute('''
        INSERT INTO passwords (service, username, password) 
        VALUES (?, ?, ?)
    ''', (service, username, encrypted_password))
    conn.commit()

    print("Password added successfully.")


def view_passwords():
    cursor.execute('SELECT * FROM passwords')
    rows = cursor.fetchall()

    for row in rows:
        service, username, encrypted_password = row
        password = decrypt_data(encrypted_password)
        print(f"Service: {service}, Username: {username}, Password: {password}")


while True:
    print("\nPassword Manager Menu:")
    print("1. Add a new password")
    print("2. View all passwords")
    print("3. Exit")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        add_password()
    elif choice == '2':
        view_passwords()
    elif choice == '3':
        print("Exiting Password Manager. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
