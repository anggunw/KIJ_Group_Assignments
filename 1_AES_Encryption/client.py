import base64
import socket
import json
import sys

from Crypto.Random import get_random_bytes
from aes_library import AESLibrary
from rsa_library import RSALibrary

TARGET_IP = "192.168.1.12"
TARGET_PORT = 8889

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (TARGET_IP, TARGET_PORT)
        self.sock.connect(self.server_address)

    def proses(self, cmdline):
        j = cmdline.split(" ")
        try:
            command = j[0].strip()
            if command == 'encrypt':
                method = j[1].strip()
                filename = j[2].strip()
                return self.encryptfile(method, filename)
            elif command == 'decrypt':
                method = j[1].strip()
                filename = j[2].strip()
                return self.decryptfile(method, filename)
            elif command == 'send':
                filename = j[1].strip()
                return self.sendfile(filename)
            elif command == 'get':
                filename = j[1].strip()
                return self.getfile(filename)
            else:
                return "*Wrong command"
        except IndexError:
            return "-Wrong command"

    def sendstring(self, string):
        try:
            self.sock.sendall(string.encode())
            receivemsg = ""
            while True:
                data = self.sock.recv(4096)
                print("Accepted from server", data)
                if data:
                    receivemsg = "{}{}" . format(receivemsg, data.decode())
                    if receivemsg[-4:] == '\r\n\r\n':
                        print("end of string")
                        return json.loads(receivemsg)
        except Exception as e:
            self.sock.close()
            return {'status': 'ERROR', 'message': str(e)}

    def encryptfile(self, method='', filename=''):
        string = "Encrypt file {} with method implemented from {} \r\n" . format(filename, method)
        print(string)
        if method == 'scratch':
            # call encrypt implementation from scratch function
            message = ""
            return message
        elif method == 'library':
            message = aeslib.encrypt(filename)
            return message
        else:
            return "Method not found"

    def decryptfile(self, method='', filename=''):
        string = "Decrypt file {} with method implemented from {} \r\n" . format(filename, method)
        print(string)
        if method == 'scratch':
            # call decrypt implementation from scratch function
            message = ""
            return message
        elif method == 'library':
            message = aeslib.decrypt(filename)
            return message
        else:
            return "Method not found"

    def sendfile(self, filename=''):
        try:
            fp = open(f"{filename}", 'rb')
            filedata = base64.b64encode(fp.read()).decode()

            string = ("send {} " . format(filename)) + filedata + " \r\n"
            print(string)

            result = self.sendstring(string)
        except Exception as e:
            return str(e)
        if result['status'] == 'OK':
            return "file {} has been sent" . format(filename)
        else:
            return "Error, {}" . format(result['message'])

    def getfile(self, filename=''):
        string = "get {} \r\n".format(filename)
        print(string)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            filename = result['filename_data']
            filedata = base64.b64decode(result['file_data'])
            fp = open(filename, 'wb+')
            fp.write(filedata)
            fp.close()
            return "received file {}".format(filename)
        else:
            return "Error, {}".format(result['message'])

if __name__ == "__main__":
    c = Client()
    key_length = 2048
    nonce = "12345678".encode()
    random_key = get_random_bytes(16)

    rsalib = RSALibrary(key_length)

    key = rsalib.generate_key()
    private_key = rsalib.private_key(key,"private.pem")
    public_key = rsalib.public_key(key,"public.pem")

    encrypt_rsa = rsalib.encrypt_rsa(random_key,"public.pem")
    decrypt_rsa = rsalib.decrypt_rsa(encrypt_rsa, "private.pem")

    # debugging code
    # print("random_key : ", random_key)    
    # print("encrypt_rsa : ", encrypt_rsa)
    # print("decrypt_rsa : ", decrypt_rsa)

    aeslib = AESLibrary(random_key, nonce)

    while True:
        cmdline = input("Command:")
        print(c.proses(cmdline))
