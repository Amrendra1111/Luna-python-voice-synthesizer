import sys
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import boto3

# Function to get the absolute path to the resource
def resource_path(relative_path):
    """ Get the absolute path to the resource in the PyInstaller bundle. """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Load the .env file
load_dotenv(resource_path('.env'))

# Function to load the encryption key
def load_key():
    with open(resource_path('encryption_key.key'), 'rb') as key_file:
        key = key_file.read()
    return key

# Function to decrypt the credentials
def decrypt_credentials(encrypted_access_key, encrypted_secret_key, key):
    cipher_suite = Fernet(key)
    decrypted_access_key = cipher_suite.decrypt(encrypted_access_key.encode()).decode()
    decrypted_secret_key = cipher_suite.decrypt(encrypted_secret_key.encode()).decode()
    return decrypted_access_key, decrypted_secret_key

# Load the encryption key
encryption_key = load_key()

# Load encrypted credentials from .env file
encrypted_access_key = os.getenv('encrypted_aws_access_key_id')
encrypted_secret_key = os.getenv('encrypted_aws_secret_access_key')

# Check if encrypted credentials are set
if not encrypted_access_key or not encrypted_secret_key:
    raise ValueError("Encrypted AWS credentials not found in .env file.")

# Decrypt the credentials
aws_access_key_id, aws_secret_access_key = decrypt_credentials(encrypted_access_key, encrypted_secret_key, encryption_key)

# Initialize the boto3 client with the decrypted credentials
polly_client = boto3.client('polly', region_name='ap-south-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def initialize_polly_client(region_name='us-east-1'):
    """Initialize the AWS Polly client."""
    return boto3.client('polly', region_name=region_name)

def synthesize_speech(polly_client, text, voice_id='Joanna', output_format='mp3'):
    """Synthesize speech using AWS Polly."""
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id
    )
    audio_stream = response['AudioStream'].read()
    return audio_stream

# Now you can use the polly_client for your operations
print("Polly client initialized successfully.")
