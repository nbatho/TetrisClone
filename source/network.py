import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.55.110"  # IP của server bạn
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
        except Exception as e:
            print(f"Connection error: {e}")

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096))  # Nhận phản hồi từ server
        except socket.error as e:
            print("Send error:", e)
            return None

    def receive(self):
        try:
            return pickle.loads(self.client.recv(4096))
        except Exception as e:
            print("Receive error:", e)
            return None