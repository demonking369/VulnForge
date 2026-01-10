from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Tuple

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def _load_key() -> bytes:
    key_b64 = os.getenv("ENCRYPTION_KEY_BASE64")
    if not key_b64:
        raise RuntimeError("ENCRYPTION_KEY_BASE64 is required")
    key = base64.b64decode(key_b64)
    if len(key) not in (16, 24, 32):
        raise ValueError("AES-GCM key must be 128/192/256-bit")
    return key


def encrypt_raw_snippet(
    plaintext: bytes, aad: bytes | None = None
) -> Tuple[bytes, bytes, bytes]:
    key = _load_key()
    aes = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aes.encrypt(nonce, plaintext, aad)
    tag = ciphertext[-16:]
    body = ciphertext[:-16]
    return body, nonce, tag


def decrypt_raw_snippet(
    ciphertext: bytes, nonce: bytes, tag: bytes, aad: bytes | None = None
) -> bytes:
    key = _load_key()
    aes = AESGCM(key)
    return aes.decrypt(nonce, ciphertext + tag, aad)
