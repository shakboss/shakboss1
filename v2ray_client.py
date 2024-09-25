import socket
import json
import base64
import hashlib

class VmessClient:
    def __init__(self, server, port, uuid):
        self.server = server
        self.port = port
        self.uuid = uuid

    def create_request(self):
        # Create a Vmess request
        request = {
            "v": "2",
            "ps": "Python Vmess Client",
            "add": self.server,
            "port": str(self.port),
            "id": self.uuid,
            "aid": "0",
            "net": "ws",
            "type": "none",
            "host": "us-23.hihu.net",
            "path": "/8znusky7",
            "tls": ""
        }
        return json.dumps(request)

    def connect(self):
        # Connect to the Vmess server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server, self.port))
            request = self.create_request()
            s.sendall(base64.b64encode(request.encode()))
            response = s.recv(1024)
            print("Response from server:", base64.b64decode(response).decode())

if __name__ == "__main__":
    # Example usage
    server = "pushplanet.com"
    port = 80
    uuid = str(hashlib.md5(b"92064570-7b70-11ef-b332-205c6d5f5d78").hexdigest())  # Replace with your actual UUID
    client = VmessClient(server, port, uuid)
    client.connect()
