import os
import base64
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC as PBKDF2

class EncryptionHandler:
    def __init__(self, password="educational_demo_2024"):
        self.password = password
        self.key = None
        self.salt = b'educational_salt_2024'
        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    
    def generate_key(self):
        try:
            # Use PBKDF2HMAC instead of PBKDF2
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.password.encode()))
            self.key = key
            self.logger.info("[KEY] Encryption key generated successfully")
            return key
        except Exception as e:
            self.logger.error(f"[ERROR] Key generation failed: {e}")
            return None
    
    def encrypt_file(self, filepath):
        if not self.key:
            self.generate_key()
        
        cipher = Fernet(self.key)
        
        try:
            with open(filepath, 'rb') as f:
                file_data = f.read()
            
            encrypted_data = cipher.encrypt(file_data)
            encrypted_path = filepath + '.encrypted'
            
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)
            
            os.remove(filepath)
            self.logger.info(f"[ENCRYPT] {os.path.basename(filepath)}")
            return encrypted_path
        except Exception as e:
            self.logger.error(f"[ERROR] Failed to encrypt {filepath}: {e}")
            return None
    
    def decrypt_file(self, encrypted_path):
        if not self.key:
            self.logger.error("[ERROR] No key loaded")
            return None
        
        cipher = Fernet(self.key)
        
        try:
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = cipher.decrypt(encrypted_data)
            original_path = encrypted_path[:-10]
            
            with open(original_path, 'wb') as f:
                f.write(decrypted_data)
            
            os.remove(encrypted_path)
            self.logger.info(f"[DECRYPT] {os.path.basename(encrypted_path)}")
            return original_path
        except Exception as e:
            self.logger.error(f"[ERROR] Failed to decrypt {encrypted_path}: {e}")
            return None
    
    def load_key(self, key=None):
        if key:
            self.key = key
        else:
            self.generate_key()
        return self.key
    
    def is_encrypted(self, filepath):
        return filepath.endswith('.encrypted')