from socket import *
import socket
import threading
import logging

from file_protocol import FileProtocol
fp = FileProtocol()


class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        rcv = ""
        while True:
            data = self.connection.recv(4096)
            if data:
                d = data.decode()
                rcv = rcv + d
                if rcv[-2:] == '\r\n':
                    # end of command, processing string
                    logging.warning("data from client: {}" . format(rcv))
                    result = fp.process_string(rcv)
                    result = result + "\r\n\r\n"
                    self.connection.sendall(result.encode())
                    rcv = ""
            else:
                break
        self.connection.close()


class Server(threading.Thread):
    def __init__(self, ipaddress='0.0.0.0', port=8889):
        self.ipinfo = (ipaddress, port)
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)

    def run(self):
        logging.warning(f"server run on ip address {self.ipinfo}")
        self.my_socket.bind(self.ipinfo)
        self.my_socket.listen(1)
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"connection from {self.client_address}")

            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)


def main():
    svr = Server(ipaddress='0.0.0.0', port=8889)
    svr.start()


if __name__ == "__main__":
    main()
