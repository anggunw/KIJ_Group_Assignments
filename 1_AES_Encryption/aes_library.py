import os
import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESLibrary:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt(self, filename):
        time_start = datetime.datetime.now()
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)

        try:
            fp = open(f"{filename}", 'rb')
            ciphertext = cipher.encrypt(pad(fp.read(), AES.block_size))
            fp.close()
        except Exception as e:
            return str(e)

        encryptedfilename = filename + ".enc"
        self.convertfile(ciphertext, filename, encryptedfilename)

        time_end = datetime.datetime.now()
        time_total = time_end - time_start
        return(f"file {filename} has been encrypted to {encryptedfilename} with total time {time_total} seconds")

    def decrypt(self, filename):
        time_start = datetime.datetime.now()
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)

        try:
            fp = open(f"{filename}", 'rb')
            plaintext = unpad(cipher.decrypt(fp.read()), AES.block_size)
            fp.close()
        except Exception as e:
            return str(e)

        decryptedfilename = filename[:-4]
        self.convertfile(plaintext, filename, decryptedfilename)

        time_end = datetime.datetime.now()
        time_total = time_end - time_start
        return(f"file {filename} has been decrypted to {decryptedfilename} with total time {time_total} seconds")

    def convertfile(self, text, fromfile, tofile):
        fp = open(f"{tofile}", 'wb+')
        fp.write(text)
        fp.close()
        os.remove(fromfile)
        return
