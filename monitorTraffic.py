import socket

# Nastavení IP adresy a portu pro naslouchání
HOST = '127.0.0.1'  # Lokální adresa
PORT = 12345        # Příkladový port, který chceme monitorovat

# Seznam blokovaných IP adres a portů
blocked_ports = [9999, 8888]  # Příkladové blokované porty

# Vytvoření soketu
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening on {HOST}:{PORT}...")

    while True:
        conn, addr = s.accept()
        ip, port = addr
        if port in blocked_ports:
            print(f"Blocked connection attempt from {ip}:{port}")
            conn.close()  # Zavření připojení, pokud je adresa/port blokována
        else:
            print(f"Connected by {ip}:{port}")
            with conn:
                data = conn.recv(1024)  # Přijetí dat od klienta
                if data:
                    conn.sendall(data)  # Echo dat zpět klientovi
                conn.close()  # Správně zavřít připojení po dokončení

# Tento skript se nyní pokouší přijímat připojení a zkontrolovat, zda je z blokované IP adresy nebo portu.
