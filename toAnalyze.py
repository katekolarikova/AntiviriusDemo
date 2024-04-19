import socket
import time

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            print(f"File content: {content}")
            time.sleep(1)

    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_network_connection(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            time.sleep(1)
            print(f"Connected to {host} on port {port}")
            s.sendall(b"GET / HTTP/1.0\r\n\r\n")
            s.recv(4096)
    except Exception as e:
        print(f"Failed to create network connection: {e}")


server_host = 'time.nist.gov'
server_port = 13
create_network_connection(server_host, server_port)
file_path = './data/nakupni_sezname.txt'
read_file(file_path)

