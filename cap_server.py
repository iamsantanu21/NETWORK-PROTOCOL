import socket

HOST = 'localhost'
PORT = 5050

def start_cap_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[DLSw-CAP Server] Listening on {HOST}:{PORT}...")

        conn, addr = server.accept()
        with conn:
            print(f"[DLSw-CAP Server] Connection from {addr}")
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break

                print(f"[DLSw-CAP Server] Received: {data}")
                
                if data == "CAP_CONNECT_REQUEST":
                    conn.sendall("CAP_CONNECT_ACK".encode())
                    print("[DLSw-CAP Server] Sent: CAP_CONNECT_ACK")
                elif data.startswith("SNA_DATA:"):
                    print(f"[DLSw-CAP Server] Received SNA data: {data[9:]}")
                    conn.sendall("SNA_DATA_ACK".encode())
                elif data == "DISCONNECT":
                    print("[DLSw-CAP Server] Disconnecting...")
                    break

if __name__ == "__main__":
    start_cap_server()
