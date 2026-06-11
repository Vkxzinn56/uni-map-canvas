"""
UniMap 3.0 - Encryption Tests
AES-256-GCM field encryption
"""
import pytest

from backend.shared.security.encryption import EncryptionService


class TestEncryptionService:
    def setup_method(self):
        self.service = EncryptionService()

    def test_encrypt_decrypt_roundtrip(self):
        plaintext = "123.456.789-00"
        encrypted = self.service.encrypt(plaintext)
        decrypted = self.service.decrypt(encrypted)
        assert decrypted == plaintext

    def test_encrypted_differs_from_plaintext(self):
        plaintext = "sensitive data"
        encrypted = self.service.encrypt(plaintext)
        assert encrypted != plaintext

    def test_same_plaintext_different_ciphertext(self):
        """AES-GCM with random nonce produces different ciphertext each time."""
        plaintext = "123.456.789-00"
        c1 = self.service.encrypt(plaintext)
        c2 = self.service.encrypt(plaintext)
        assert c1 != c2

    def test_both_decrypt_to_same_plaintext(self):
        plaintext = "test@email.com"
        c1 = self.service.encrypt(plaintext)
        c2 = self.service.encrypt(plaintext)
        assert self.service.decrypt(c1) == self.service.decrypt(c2) == plaintext

    def test_encrypt_optional_none(self):
        assert self.service.encrypt_optional(None) is None

    def test_decrypt_optional_none(self):
        assert self.service.decrypt_optional(None) is None

    def test_encrypt_optional_value(self):
        result = self.service.encrypt_optional("test")
        assert result is not None
        assert self.service.decrypt(result) == "test"

    def test_hash_sensitive_deterministic(self):
        """Same input always hashes to same value (for lookup)."""
        cpf = "123.456.789-00"
        h1 = self.service.hash_sensitive(cpf)
        h2 = self.service.hash_sensitive(cpf)
        assert h1 == h2

    def test_hash_different_inputs_differ(self):
        h1 = self.service.hash_sensitive("111.222.333-44")
        h2 = self.service.hash_sensitive("555.666.777-88")
        assert h1 != h2

    def test_tampered_ciphertext_raises(self):
        plaintext = "important data"
        encrypted = self.service.encrypt(plaintext)
        # Tamper with the ciphertext
        tampered = encrypted[:-4] + "XXXX"
        with pytest.raises(Exception):
            self.service.decrypt(tampered)

    def test_long_string_encryption(self):
        """Test with a realistic address JSON string."""
        import json
        address = json.dumps({
            "street": "Rua das Flores, 123",
            "city": "São Paulo",
            "state": "SP",
            "zip": "01310-100",
            "complement": "Apto 42"
        })
        encrypted = self.service.encrypt(address)
        decrypted = self.service.decrypt(encrypted)
        assert json.loads(decrypted)["city"] == "São Paulo"
