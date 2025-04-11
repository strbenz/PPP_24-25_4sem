import socket
import ssl
import logging

HOST = '127.0.0.1'
PORT = 12345

logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def send_data(conn, data):
    if isinstance(data, str):
        data = data.encode()
    length = f"{len(data):010}".encode()
    conn.sendall(length + data)

def recv_data(conn):
    header = b""
    while len(header) < 10:
        chunk = conn.recv(10 - len(header))
        if not chunk:
            break
        header += chunk
    if not header:
        return None
    length = int(header.decode())
    data = b""
    while len(data) < length:
        chunk = conn.recv(length - len(data))
        if not chunk:
            break
        data += chunk
    return data.decode()

def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=HOST) as ssock:
            while True:
                cmd = input("Введите команду (UPDATE, SETENV var value, LIST [criteria], EXIT): ")
                if cmd.upper() == "EXIT":
                    break
                send_data(ssock, cmd)
                logging.info(f"Sent command: {cmd}")
                response = recv_data(ssock)
                logging.info("Received response")
                print("Ответ от сервера:")
                print(response)

if __name__ == "__main__":
    main()
