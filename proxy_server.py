import socket, time, sys
import multiprocessing

# server -> connects to google -> sends the request from a client
# client -> connects to server with request -> server sends request to google
# google sends response back to server -> which sends it back to the client

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

# create the tcp socket
def create_tcp_socket():
    print(f"getting the ip address")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        print("couldn't create socket")
        sys.exit()
    return s


#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")


def handle_request(buffer_size, start_socket, end_socket):
#recieve data, wait a bit, then send it back
    full_data = end_socket.recv(buffer_size)
    full_data = full_data.decode('utf-8')
    print("Client sent this: ", full_data)
    time.sleep(0.5)

    # send client request to google
    send_data(start_socket, full_data)
    start_socket.shutdown(socket.SHUT_WR)

    # get back response from google
    google_data = b""
    while True:
        data_1 = start_socket.recv(buffer_size)
        if not data_1:
            break
        google_data += data_1
    # return response from google back to client (conn is client)
    end_socket.sendall(google_data)


def main():
    try:
        #define address info, payload, and buffer size
        host = 'www.google.com'
        port = 80
        payload = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'
        buffer_size = 1024
        HOST_PROXY = '127.0.0.1'
        PORT_PROXY = 8001
        # listen for requests from client and accept the connection s = local socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST_PROXY, PORT_PROXY))
            s.listen(5)
            while True:
                # conn is the return socket to the client 
                conn, addr = s.accept()
                print("Connected by", addr)
                # google socket is the connection to between server and google
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as google_socket:
                    remote_ip = get_remote_ip(host)
                    google_socket.connect((remote_ip, port))
                    # start muultiprocess
                    p = multiprocessing.Process(target=handle_request, args=(buffer_size, google_socket, conn))
                    p.daemon = True
                    p.start()
                conn.close()

    except:
        pass


if __name__ == "__main__":
    main()

    

