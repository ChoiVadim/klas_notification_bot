from cryptography.fernet import Fernet


# Step 1: Generate and save the key (do this once)
def generate_key():
    key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)


# Step 2: Load the key
def load_key():
    with open("encryption_key.key", "rb") as key_file:
        return key_file.read()


# Step 3: Encrypt data
def encrypt_password(password):
    cipher = Fernet(load_key())
    return cipher.encrypt(password.encode())


# Step 4: Decrypt data
def decrypt_password(encrypted_password):
    cipher = Fernet(load_key())
    return cipher.decrypt(encrypted_password).decode()


if __name__ == "__main__":
    # generate_key()

    password = "my_secure_password"
    encrypted = encrypt_password(password)
    print("Encrypted:", encrypted)

    decrypted = decrypt_password(encrypted)
    print("Decrypted:", decrypted)
