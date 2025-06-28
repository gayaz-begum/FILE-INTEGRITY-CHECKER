import hashlib
import os
import json

# Function to calculate file hash
def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

# Function to save hash to JSON
def save_hash(file_path, hash_value):
    data = {file_path: hash_value}
    with open("file_hashes.json", "w") as f:
        json.dump(data, f, indent=4)

# Function to check file integrity
def check_integrity(file_path):
    current_hash = calculate_hash(file_path)
    try:
        with open("file_hashes.json", "r") as f:
            saved_hashes = json.load(f)
    except FileNotFoundError:
        print("Hash file not found. Save the hash first.")
        return

    if file_path in saved_hashes:
        if saved_hashes[file_path] == current_hash:
            print("✅ File integrity verified. No changes detected.")
        else:
            print("⚠️ WARNING: File has been modified!")
    else:
        print("File not found in saved hash records.")

# Main Execution
if __name__ == "__main__":
    print("1. Save file hash")
    print("2. Check file integrity")
    choice = input("Enter choice (1/2): ")
    path = input("Enter file path: ")

    if choice == "1":
        h = calculate_hash(path)
        if h:
            save_hash(path, h)
            print("Hash saved.")
    elif choice == "2":
        check_integrity(path)
    else:
        print("Invalid choice.")