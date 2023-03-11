"""
Use this script to generate an RSA private key and prints it
to the standard output. The generated private key is in the
PKCS#8 format with no encryption.
"""

from base64 import urlsafe_b64encode

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
serialized_private_key = private_key.private_bytes(
    serialization.Encoding.PEM,
    serialization.PrivateFormat.PKCS8,
    serialization.NoEncryption(),
)

# set the printed value in .env
print(urlsafe_b64encode(serialized_private_key).decode())
