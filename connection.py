import socket
import struct


class Connection:
    LEN_SIZE = 4
    BUFFER_SIZE = 4096

    def __init__(self, connection: socket.socket):
        self.connection = connection

    def __repr__(self):
        (server_ip, server_port) = self.connection.getsockname()
        (client_ip, client_port) = self.connection.getpeername()
        return f"<Connection from {client_ip}:{client_port} to {server_ip}:{server_port}"

    def send_message(self, data: str):
        msg = data.encode("utf-8")
        msg_len = len(msg)
        encoded_len = struct.pack("<I", msg_len)
        self.connection.send(encoded_len + msg)

    def receive_message(self):
        try:
            encoded_len = self.connection.recv(self.LEN_SIZE)
            if encoded_len:
                msg_len = struct.unpack("<I", encoded_len)[0]
                msg = self.connection.recv(msg_len).decode('utf8')
                return msg
        except Exception as error:
            print("Error: ", error)

    @classmethod
    def connect(cls, host: str, port: int):
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv.connect((host, port))
        return Connection(serv)

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
