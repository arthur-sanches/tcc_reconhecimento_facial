import socket

HEADERSIZE = 10


def establish_connection():  # (operador):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 6418))
    return s
    #s.connect(operador, 6416)
    #print("Connection established with " + operador + " on port 6416")


def close_connection(s):
    send_message(s, "close conn")
    s.close()
    print("Connection closed.")


def send_message(s, log):
    log = f"{len(log):<{HEADERSIZE}}" + log
    s.send(bytes(log, "utf-8"))

def send_image(s):
    pass

def recv_encodings(s):
    full_enc = ''
    new_enc = True
    while True:
        enc = s.recv(32)

        if len(enc) == 0:
            return('')

        if new_enc:
            enclen = int(enc[:HEADERSIZE])
            new_enc = False

        full_enc += enc.decode("utf-8")

        if len(full_enc[HEADERSIZE:]) == enclen:
            print("Encoding received!")
            return(full_enc)
