import socket

HOST = '127.0.0.1'
PORT = 8001
host = 'www.google.com'
payload = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(payload.encode())
    s.shutdown(socket.SHUT_WR)
    # get data back
    full_data = b""
    while True:
        data = s.recv(1024)
        if not data:
            break
        full_data += data
    print(full_data)
    s.close()

# print('recieved'), repr(data)