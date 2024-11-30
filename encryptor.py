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


def encrypt_user_data(user_data):
    encrypted_data = {}
    for user_id, user_info in user_data.items():
        encrypted_data[user_id] = {
            "username": encrypt_password(user_info["username"]),
            "password": encrypt_password(user_info["password"]),
        }
    return encrypted_data


def decrypt_user_data(encrypted_data):
    decrypted_data = {}
    for user_id, user_info in encrypted_data.items():
        decrypted_data[user_id] = {
            "username": decrypt_password(user_info["username"]),
            "password": decrypt_password(user_info["password"]),
        }
    return decrypted_data


# Example usage
if __name__ == "__main__":
    # Generate key (only once, comment after first run)
    # generate_key()

    # Encrypt and decrypt a password
    # password = "my_secure_password"
    # encrypted = encrypt_password(password)
    # print("Encrypted:", encrypted)

    # decrypted = decrypt_password(encrypted)
    # print("Decrypted:", decrypted)
    user_data = {"1815092465": {"username": "2022203502", "password": "example"}}
    encrypted_data = encrypt_user_data(user_data)
    print(encrypted_data)

    decrypted_data = decrypt_user_data(encrypted_data)
    print(decrypted_data)
