#!/usr/bin/env python3
import socket
import time
import multiprocessing

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

# function to echo back what was recieved
def handle_echo(end_socket, buffer_size):
    full_data = end_socket.recv(BUFFER_SIZE)
    print(full_data)
    time.sleep(0.5)
    end_socket.sendall(full_data)
    end_socket.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            #recieve data, wait a bit, then send it back
            # handle echo function
            p = multiprocessing.Process(target=handle_echo, args=(conn, BUFFER_SIZE))
            p.daemon = True
            p.start()


if __name__ == "__main__":
    main()
