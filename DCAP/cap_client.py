import socket
import time

HOST = 'localhost'
PORT = 5050

def start_cap_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print("[CAP Client] Connected to DLSw-CAP Server.")

        # Step 1: Send CAP connect request
        client.sendall("CAP_CONNECT_REQUEST".encode())
        print("[CAP Client] Sent: CAP_CONNECT_REQUEST")

        # Step 2: Wait for ACK
        ack = client.recv(1024).decode()
        print(f"[CAP Client] Received: {ack}")

        if ack == "CAP_CONNECT_ACK":
            # Step 3: Exchange mock SNA data
            for i in range(3):
                sna_data = f"SNA_DATA:Hello_Frame_{i+1}"
                print(f"[CAP Client] Sending SNA data: {sna_data}")
                client.sendall(sna_data.encode())
                response = client.recv(1024).decode()
                print(f"[CAP Client] Server response: {response}")
                time.sleep(1)

        # Step 4: Disconnect
        client.sendall("DISCONNECT".encode())
        print("[CAP Client] Sent: DISCONNECT")

if __name__ == "__main__":
    start_cap_client()
