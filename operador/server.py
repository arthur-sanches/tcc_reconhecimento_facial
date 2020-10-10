import socket
import time

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 6416))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    full_log = ''
    new_log = True
    while True:
        log = clientsocket.recv(32)

        if new_log:
            loglen = int(log[:HEADERSIZE])
            new_log = False

        full_log += log.decode("utf-8")
        cleaned_log = full_log[HEADERSIZE:]

        if cleaned_log == b'close conn':
            break

        if len(cleaned_log) == loglen:
            print("Log received!")
            print(cleaned_log)
            with open("operador/logs.txt", "a") as f:
                f.write(cleaned_log+'\n')
            full_log = ''
            new_log = True
