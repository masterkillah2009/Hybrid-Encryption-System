import os
from cryptography.fernet import Fernet
import rsa

def generate_keys():
    public_key, private_key = rsa.newkeys(2048)
    with open("public.pem", "wb") as f:
        f.write(public_key.save_pkcs1("PEM"))
    with open("private.pem", "wb") as f:
        f.write(private_key.save_pkcs1("PEM"))
    print("RSA public and private keys generated and saved successfully.")
    return public_key, private_key

def encrypt(file_to_encrypt, public_key):
    if not os.path.exists(file_to_encrypt):
        raise FileNotFoundError(f"File '{file_to_encrypt}' does not exist.")
    try:
        # Generate symmetric key
        symmetric_key = Fernet.generate_key()
        with open("symmetric.key", "wb") as key_file:
            key_file.write(symmetric_key)
        print("Fernet symmetric key generated and saved to 'symmetric.key' successfully.")
        with open(file_to_encrypt, "rb") as f:
            original_file_content = f.read()
        fernet = Fernet(symmetric_key)
        encrypted_file_content = fernet.encrypt(original_file_content)
        encrypted_symmetric_key = rsa.encrypt(symmetric_key, public_key)
        encrypted_file_name = file_to_encrypt + ".encrypted"
        with open(encrypted_file_name, "wb") as f:
            f.write(encrypted_file_content)
        encrypted_symmetric_key_name = "symmetric.key.encrypted"
        with open(encrypted_symmetric_key_name, "wb") as f:
            f.write(encrypted_symmetric_key)
        print(f"File '{file_to_encrypt}' encrypted and saved as '{encrypted_file_name}'.")
        print(f"Symmetric key encrypted and saved as '{encrypted_symmetric_key_name}'.")
        return encrypted_file_name, encrypted_symmetric_key_name
    except Exception as e:
        print(f"Error during encryption: {e}")
        raise

def decrypt(encrypted_file_name, encrypted_symmetric_key_name, private_key, original_file_name):
    if not os.path.exists(encrypted_file_name):
        raise FileNotFoundError(f"Encrypted file '{encrypted_file_name}' does not exist.")
    if not os.path.exists(encrypted_symmetric_key_name):
        raise FileNotFoundError(f"Encrypted key file '{encrypted_symmetric_key_name}' does not exist.")
    try:
        with open(encrypted_symmetric_key_name, "rb") as key_file:
            encrypted_symmetric_key_loaded = key_file.read()
        decrypted_symmetric_key = rsa.decrypt(encrypted_symmetric_key_loaded, private_key)
        print("Symmetric key decrypted successfully!")
        with open(encrypted_file_name, "rb") as f:
            encrypted_file_content_loaded = f.read()
        fernet_decryptor = Fernet(decrypted_symmetric_key)
        decrypted_file_content = fernet_decryptor.decrypt(encrypted_file_content_loaded)
        decrypted_file_name = original_file_name + ".decrypted"
        with open(decrypted_file_name, "wb") as f:
            f.write(decrypted_file_content)
        print(f"File '{encrypted_file_name}' decrypted and saved as '{decrypted_file_name}'.")
        # Verification
        with open(original_file_name, "rb") as f:
            original_content = f.read()
        with open(decrypted_file_name, "rb") as f:
            decrypted_content = f.read()
        if original_content == decrypted_content:
            print("Verification successful: Decrypted content matches original content!")
        else:
            print("Verification failed: Decrypted content DOES NOT match original content.")
    except Exception as e:
        print(f"Error during decryption: {e}")
        raise

if __name__ == "__main__":
    public_key, private_key = generate_keys()
    file_to_encrypt = input("Enter the file you'd like to encrypt/decrypt: ")
    choice = input("Enter 'e' to encrypt or 'd' to decrypt: ").lower()
    if choice == 'e':
        encrypted_file_name, encrypted_symmetric_key_name = encrypt(file_to_encrypt, public_key)
    elif choice == 'd':
        # Assume encrypted files exist with standard names
        encrypted_file_name = file_to_encrypt + ".encrypted"
        encrypted_symmetric_key_name = "symmetric.key.encrypted"
        decrypt(encrypted_file_name, encrypted_symmetric_key_name, private_key, file_to_encrypt)
    else:
        print("Invalid choice.")
