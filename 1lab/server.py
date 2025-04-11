import os, json, socket, ssl, logging, time

HOST = '127.0.0.1'
PORT = 12345

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def scan_executables():
    path_env = os.environ.get("РАТН", "")
    tree = {}
    for d in path_env.split(os.pathsep):
        if os.path.isdir(d):
            executables = []
            try:
                for f in os.listdir(d):
                    full_path = os.path.join(d, f)
                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                        st = os.stat(full_path)
                        executables.append({"name": f, "size": st.st_size, "mod_date": st.st_mtime})
            except Exception as e:
                logging.error(f"Error scanning {d}: {e}")
            tree[d] = executables
    return tree

def update_info():
    tree = scan_executables()
    with open("env_info.json", "w") as f:
        json.dump(tree, f)
    return tree

def log_env_change(var, value):
    with open("env_history.log", "a") as f:
        f.write(f"{time.ctime()}: {var}={value}\n")

def handle_command(cmd):
    parts = cmd.strip().split()
    if not parts:
        return "Empty command"
    if parts[0].upper() == "UPDATE":
        tree = update_info()
        logging.info("Updated info")
        return json.dumps(tree)
    elif parts[0].upper() == "SETENV" and len(parts) >= 3:
        var = parts[1]
        value = " ".join(parts[2:])
        os.environ[var] = value
        log_env_change(var, value)
        logging.info(f"Set env {var}={value}")
        return f"Переменная окружения {var} установлена в {value}"
    elif parts[0].upper() == "LIST":
        tree = scan_executables()
        lst = []
        for d, files in tree.items():
            for f in files:
                f['dir'] = d
                lst.append(f)
        if len(parts) > 1:
            key = parts[1]
            if key in ["name", "size", "mod_date"]:
                lst.sort(key=lambda x: x[key])
        return json.dumps(lst)
    else:
        return "Неизвестная команда"

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
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        logging.info(f"Server started on {HOST}:{PORT}")
        while True:
            conn, addr = sock.accept()
            logging.info(f"Connection from {addr}")
            try:
                with context.wrap_socket(conn, server_side=True) as ssock:
                    while True:
                        cmd = recv_data(ssock)
                        if cmd is None:
                            break
                        logging.info(f"Received command: {cmd}")
                        response = handle_command(cmd)
                        send_data(ssock, response)
            except Exception as e:
                logging.error(f"Connection error: {e}")

if __name__ == "__main__":
    main()
