# Hybrid-Encryption-System



# Hybrid File Encryption Tool

A Python-based tool for secure file encryption and decryption using **hybrid cryptography**. This combines **RSA asymmetric encryption** for the key exchange and **Fernet symmetric encryption** for encrypting file content. Ideal for securely sharing files without exposing the raw symmetric key.

---

## Features

* Generates **RSA key pairs** (public and private) for encryption and decryption.
* Uses **Fernet symmetric encryption** for fast and secure file encryption.
* Encrypts the symmetric key with RSA for safe storage.
* Decrypts files and verifies that the decrypted content matches the original file.

---

## Requirements

* Python 3.8+
* [cryptography](https://pypi.org/project/cryptography/)
* [rsa](https://pypi.org/project/rsa/)

Install dependencies via pip:

```bash
pip install cryptography rsa
```

---

## Usage

1. **Run the script**:

```bash
python your_script_name.py
```

2. **Generate keys**:
   The script will automatically generate `public.pem` and `private.pem` in the current directory.

3. **Encrypt a file**:

* Enter the file path when prompted.
* Choose `e` for encryption.
* Outputs:

  * Encrypted file: `<filename>.encrypted`
  * Encrypted symmetric key: `symmetric.key.encrypted`
  * Original symmetric key: `symmetric.key` (optional backup)

4. **Decrypt a file**:

* Enter the original file name (without `.encrypted`) when prompted.
* Choose `d` for decryption.
* Outputs:

  * Decrypted file: `<filename>.decrypted`
* The script verifies that the decrypted content matches the original file.

---

## Example

```bash
Enter the file you'd like to encrypt/decrypt: secret.txt
Enter 'e' to encrypt or 'd' to decrypt: e
```

* Encrypts `secret.txt` → `secret.txt.encrypted`
* Saves symmetric key → `symmetric.key.encrypted`

```bash
Enter the file you'd like to encrypt/decrypt: secret.txt
Enter 'e' to encrypt or 'd' to decrypt: d
```

* Decrypts `secret.txt.encrypted` → `secret.txt.decrypted`
* Verification confirms integrity.

---

## Notes

* RSA keys are **2048-bit** by default.
* Make sure to **keep `private.pem` safe**, as it is required for decryption.
* Symmetric key file (`symmetric.key`) should not be shared publicly unless encrypted with RSA.

---

## Security

This hybrid approach ensures:

* **Speed**: Symmetric encryption is fast for large files.
* **Security**: RSA secures the symmetric key during transfer.
* **Integrity**: The script verifies the decrypted file against the original.

