import socket

# address and port for the listening socket
HOST = '127.0.0.1'
PORT = 12345

# List of blocked ports
blocked_ports = [9999, 8888]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening on {HOST}:{PORT}...")

    while True:  # Vytvoření nekonečné smyčky pro přijímání připojení
        conn, addr = s.accept()
        ip, port = addr
        if port in blocked_ports:  # check if the port is blocked
            print(f"Blocked connection attempt from {ip}:{port}")
            conn.close()  # if so, close the connection
        else:
            # accept the connection
            print(f"Connected by {ip}:{port}")
            with conn:
                data = conn.recv(1024)  # receive data from the client
                if data:
                    conn.sendall(data)  # send the data back to the client
                conn.close()  # close the connection
