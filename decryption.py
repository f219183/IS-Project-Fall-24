import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def decrypt_data(ciphertext, key):
    """
    Decrypts the given ciphertext using AES encryption in CBC mode.

    Args:
        ciphertext (bytes): The encrypted data to decrypt.
        key (bytes): The decryption key (must be 16, 24, or 32 bytes long).

    Returns:
        str: The decrypted plaintext.
    """
    try:
        # Decode the base64-encoded ciphertext
        ciphertext = base64.b64decode(ciphertext)

        # Separate the IV from the ciphertext
        iv = ciphertext[:16]  # First 16 bytes are the IV
        encrypted_message = ciphertext[16:]

        # Create AES cipher in CBC mode
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the message
        padded_plaintext = decryptor.update(encrypted_message) + decryptor.finalize()

        # Unpad the plaintext
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext.decode('utf-8')

    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

if __name__ == "__main__":
    # Example ciphertext and key (replace these with your values)
    encrypted_data = input("Enter the base64-encoded ciphertext: ")
    decryption_key = input("Enter the decryption key (16, 24, or 32 characters): ").encode('utf-8')

    # Validate key length
    if len(decryption_key) not in (16, 24, 32):
        print("Invalid key length. Key must be 16, 24, or 32 characters long.")
    else:
        # Perform decryption
        plaintext = decrypt_data(encrypted_data, decryption_key)
        if plaintext:
            print(f"Decrypted plaintext: {plaintext}")
