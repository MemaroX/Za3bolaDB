import ssl
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

def generate_test_certs(cert_path='test_server.crt', key_path='test_server.key'):
    # Generate Key
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    with open(key_path, 'wb') as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Generate Cert
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'localhost'),
    ])
    cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(datetime.utcnow()).not_valid_after(datetime.utcnow() + timedelta(days=1)).add_extension(x509.SubjectAlternativeName([x509.DNSName(u'localhost')]), critical=False).sign(key, hashes.SHA256())

    with open(cert_path, 'wb') as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    return cert_path, key_path

def cleanup_test_certs(cert_path='test_server.crt', key_path='test_server.key'):
    if os.path.exists(cert_path): os.remove(cert_path)
    if os.path.exists(key_path): os.remove(key_path)
