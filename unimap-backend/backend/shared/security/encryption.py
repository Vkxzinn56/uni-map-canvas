"""
UniMap 3.0 - Encryption Service
Security: AES-256-GCM for sensitive fields (CPF, address, RGM)
LGPD Compliant
"""
import base64
import hashlib
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from backend.core.config.settings import settings


class EncryptionService:
    """
    AES-256-GCM authenticated encryption.
    - Random 96-bit nonce per operation
    - 256-bit key derived from settings
    - Tag authentication included in ciphertext
    """

    def __init__(self) -> None:
        raw_key = settings.ENCRYPTION_KEY.encode()
        # Derive exactly 32 bytes (256 bits) from the configured key
        self._key = hashlib.sha256(raw_key).digest()
        self._aesgcm = AESGCM(self._key)

    def encrypt(self, plaintext: str) -> str:
        """Encrypt and return base64-encoded nonce+ciphertext."""
        nonce = os.urandom(12)  # 96-bit nonce
        ciphertext = self._aesgcm.encrypt(nonce, plaintext.encode(), None)
        combined = nonce + ciphertext
        return base64.b64encode(combined).decode()

    def decrypt(self, encrypted: str) -> str:
        """Decrypt base64-encoded nonce+ciphertext."""
        combined = base64.b64decode(encrypted.encode())
        nonce = combined[:12]
        ciphertext = combined[12:]
        plaintext = self._aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode()

    def encrypt_optional(self, value: str | None) -> str | None:
        if value is None:
            return None
        return self.encrypt(value)

    def decrypt_optional(self, value: str | None) -> str | None:
        if value is None:
            return None
        return self.decrypt(value)

    def hash_sensitive(self, value: str) -> str:
        """One-way hash for searchable sensitive fields (e.g., CPF lookup)."""
        return hashlib.sha256(
            f"{value}{settings.SECRET_KEY}".encode()
        ).hexdigest()


# Singleton
encryption_service = EncryptionService()
