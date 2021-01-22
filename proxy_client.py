import socket
from multiprocessing import Pool


def establish_connection(host):
    HOST = '127.0.0.1'
    PORT = 8001
    host = host
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


def main():
    with Pool() as p:
        arg = ['www.google.com']
        p.map(establish_connection, (arg*7))



if __name__ == "__main__":
    main()


