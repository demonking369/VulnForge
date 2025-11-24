from ..crypto import decrypt_raw_snippet, encrypt_raw_snippet


def test_encrypt_decrypt_roundtrip():
    plaintext = b"secret data"
    ciphertext, nonce, tag = encrypt_raw_snippet(plaintext)
    recovered = decrypt_raw_snippet(ciphertext, nonce, tag)
    assert recovered == plaintext

