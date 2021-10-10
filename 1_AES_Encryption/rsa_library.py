import os
import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class RSALibrary:
    def __init__(self, key_length):
        self.key_length = key_length
    
    def generate_key(self):
        key = RSA.generate(self.key_length)
        return key
        
    def private_key(self, key, filename):
        time_start = datetime.datetime.now()
        private_key = key.export_key()

        try:
            fp = open(f"{filename}", "wb")
            fp.write(private_key)
            fp.close()
        except Exception as e:
            return str(e)    

        time_end = datetime.datetime.now()
        time_total = time_end - time_start
        return(f"file private.pem has been generated with total time {time_total} seconds")

    def public_key(self, key, filename):   
        time_start = datetime.datetime.now()
        public_key = key.publickey().export_key()

        try:        
            fp = open(f"{filename}", "wb")
            fp.write(public_key)
            fp.close()
        except Exception as e:
            return str(e)  

        time_end = datetime.datetime.now()
        time_total = time_end - time_start
        return(f"file public.pem has been generated with total time {time_total} seconds")

    def encrypt_rsa(self, key, filename):
        public_key = RSA.import_key(open(f"{filename}").read())
        cipher_rsa = PKCS1_OAEP.new(public_key)
        encrypt_key = cipher_rsa.encrypt(key)
        return encrypt_key

    def decrypt_rsa(self, key, filename):
        private_key = RSA.import_key(open(f"{filename}").read())
        cipher_rsa = PKCS1_OAEP.new(private_key)
        decrypt_key = cipher_rsa.decrypt(key)
        return decrypt_key        