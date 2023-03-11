""" 
This file contains the high-level cryptographic utilities needed by
simaster.ics. The functions defined here are used internally by the views to
decrypt user-supplied encrypted password or to generate a cache key for reusing
session.
"""

import base64
import hashlib

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import types, padding


def read_private_bytes_from_b64(private_bytes: str) -> types.PRIVATE_KEY_TYPES:
    """Load private key in PEM format from a Base64-encoded (urlsafe) string"""
    decoded_pem = base64.urlsafe_b64decode(private_bytes)
    private_key = serialization.load_pem_private_key(decoded_pem, password=None)
    return private_key


def derive_serialized_public_key(private_key: types.PRIVATE_KEY_TYPES) -> str:
    """Generates a serialized public key"""
    public_key = private_key.public_key()
    serialized = public_key.public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return serialized.decode()


def decrypt_b64_password(
    private_key: types.PRIVATE_KEY_TYPES, b64_password: str
) -> str:
    """Decrypts a Base64-encoded (urlsafe) encrypted password (from JSEncrypt,
    with PKCS1v15 padding)"""
    encrypted_password = base64.urlsafe_b64decode(b64_password)
    plaintext_password = private_key.decrypt(
        encrypted_password,
        padding.PKCS1v15(),
    )
    return plaintext_password


def get_cache_key(username: str, password: str) -> str:
    """Generate a cache key for safer session caching"""
    data = f"{username}{password}"
    password_hash = hashlib.sha256(data.encode()).hexdigest()
    return password_hash
