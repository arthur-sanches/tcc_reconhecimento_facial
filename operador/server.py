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

        if len(full_log[HEADERSIZE:]) == loglen:
            print("Log received!")
            print(full_log)
            full_log = ''
            new_log = True

"""    msg = "Welcome to the server!"
    msg = f"{len(msg):<{HEADERSIZE}}" + msg

    clientsocket.send(bytes(msg, "utf-8"))

    while True:
        time.sleep(3)
        msg = f"The time is {time.time()}"
        msg = f"{len(msg):<{HEADERSIZE}}" + msg
        clientsocket.send(bytes(msg, "utf-8"))"""