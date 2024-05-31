from cryptography.fernet import Fernet
import os

def load_key():
    # Load the previously generated key
    with open('encryption_key.key', 'rb') as key_file:
        key = key_file.read()
    return key

def encrypt_credentials(aws_access_key_id, aws_secret_access_key, key):
    cipher_suite = Fernet(key)
    encrypted_access_key = cipher_suite.encrypt(aws_access_key_id.encode()).decode()
    encrypted_secret_key = cipher_suite.encrypt(aws_secret_access_key.encode()).decode()
    return encrypted_access_key, encrypted_secret_key

def write_encrypted_credentials(encrypted_access_key, encrypted_secret_key):
    with open('.env', 'w') as f:
        f.write(f'encrypted_aws_access_key_id = {encrypted_access_key}\n')
        f.write(f'encrypted_aws_secret_access_key = {encrypted_secret_key}\n')

# Get AWS credentials from environment variables
aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')

# Load the encryption key
encryption_key = load_key()

# Encrypt the credentials
encrypted_access_key, encrypted_secret_key = encrypt_credentials(aws_access_key_id, aws_secret_access_key, encryption_key)

# Write the encrypted credentials to the .env file
write_encrypted_credentials(encrypted_access_key, encrypted_secret_key)
