import re
import hashlib
import getpass
import os

FILE_NAME = "secure_file.txt" 
PASS_FILE = "password.txt"     


if not os.path.exists(PASS_FILE):
    while True:
        password = getpass.getpass("Enter new password: ")
        error = []

        if len(password) < 8:
            error.append("❌ Password must be at least 8 characters")
        if not re.search(r"[A-Z]", password):
            error.append("❌ Must include at least ONE uppercase letter")
        if not re.search(r"[a-z]", password):
            error.append("❌ Must include at least ONE lowercase letter")
        if not re.search(r"\d", password):
            error.append("❌ Must include at least ONE number")
        if not re.search(r"[!@#$%^&*]", password):
            error.append("❌ Must include at least ONE special character")

        if error:
            print("\n".join(error))
            continue

        pass_confirm = getpass.getpass("Please confirm your password: ")
        if pass_confirm != password:
            print("❌ Passwords do not match. Try again.")
            continue

       
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        with open(PASS_FILE, "w") as f:
            f.write(hashed_password)

        print("✅ Password successfully created!")
        break
else:
    print("Password already set. Proceed to login.")


with open(PASS_FILE, "r") as f:
    stored_hash = f.read()

attempts = 4
while attempts > 0:
    access_type = getpass.getpass("Enter password to access the file: ")
    hashed_attempt = hashlib.sha256(access_type.encode()).hexdigest()

    if hashed_attempt == stored_hash:
        print("✅ Access Granted")
        break
    else:
        attempts -= 1
        print(f"❌ Access Denied ({attempts} attempts left)")

if attempts == 0:
    print("🚫 Too many failed attempts. System locked.")
    exit()


while True:
    action = input("Do you want to [R]ead or [W]rite the file? ").strip().upper()
    if action == "R":
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as f:
                content = f.read()
            print("\n--- File Content ---")
            print(content)
            print("-------------------\n")
        else:
            print("File is empty.")
    elif action == "W":
        new_content = input("Enter text to write into the file: ")
        with open(FILE_NAME, "w") as f:
            f.write(new_content)
        print("✅ File updated successfully!\n")
    else:
        print("❌ Invalid option. Choose R or W.")

    cont = input("Do you want to continue? (Y/N): ").strip().upper()
    if cont != "Y":
        print("Exiting secure file system.")
        break