import ssl
import socket
from datetime import datetime

# List of known weak ciphers
WEAK_CIPHERS = ["RC4", "DES", "3DES", "MD5", "NULL", "EXPORT", "CBC"]

# Function to check SSL/TLS configuration
def evaluate_ssl_tls(hostname, port=443):
    try:
        # Establish a connection to the server
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Retrieve certificate details
                cert = ssock.getpeercert()
                print(f"Connected to {hostname}:{port}")
                print("\nCertificate Details:")
                issuer = cert.get("issuer")
                validity_start = datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y GMT")
                validity_end = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y GMT")
                print(f"  Issuer: {issuer}")
                print(f"  Validity: {validity_start} to {validity_end}")
                if validity_end < datetime.now():
                    print("  [WARNING] Certificate is expired!")

                # Check protocol and cipher
                cipher = ssock.cipher()
                protocol, cipher_suite, _ = cipher
                print("\nConnection Details:")
                print(f"  Protocol: {protocol}")
                print(f"  Cipher: {cipher_suite}")
                if any(weak_cipher in cipher_suite.upper() for weak_cipher in WEAK_CIPHERS):
                    print(f"  [WARNING] Weak cipher detected: {cipher_suite}")
                else:
                    print("  NO Weak cipher detected. Cipher is secure.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    hostname = input("Enter the hostname or IP address: ")
    evaluate_ssl_tls(hostname)
