import os.path
import socket
import time
import pickle

HEADERSIZE = 10


def cria_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_indisponivel = True
    while server_indisponivel:
        time.sleep(5)
        server_indisponivel = estabelece_conexao(s)
    return s


def estabelece_conexao(s):
    try:
        s.connect((socket.gethostname(), 6416))
        print("Conexão com servidor estabelecida!")
        return False
    except:
        print("Servidor indisponível.")
        return True
    finally:
        pass


def close_connection(s):
    send_message(s, "close conn")
    s.close()
    print("Conexão encerrada.")


def send_log(s, log):
    log = "new log:" + log
    send_message(s, log)


def send_message(s, msg):
    msg = f"{len(msg):<{HEADERSIZE}}" + msg
    try:
        s.send(bytes(msg, "utf-8"))
    except:
        s.close()
        print("Sem conexão com servidor.")
    finally:
        pass


def send_image(s, frame):
    frame_msg = str(frame)
    msg = "new img:" + frame_msg
    send_message(s, msg)


def recv_message(cliente_ligado, fila_mensagens, fila_encodings, fila_porta):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.15.13", 6416))
    s.setblocking(False)
    full_msg = ''
    new_msg = True
    while cliente_ligado:
        time.sleep(0.0125)
        try:
            msg = s.recv(4096)

            if new_msg:
                msg_len = int(msg[:HEADERSIZE])
                new_msg = False

            full_msg += msg.decode("utf-8")
            cleaned_msg = full_msg[HEADERSIZE:]
            if len(cleaned_msg) == msg_len:
                print("Messagem recebida!")
                if cleaned_msg.startswith("new enc:"):
                    recebe_encoding(cleaned_msg, fila_encodings)
                elif cleaned_msg.startswith("enco dt:"):
                    envia_data_encoding(s)
                elif cleaned_msg.startswith("end con:"):
                    close_connection(s)
                elif cleaned_msg.startswith("abr prt:"):
                    print("Abrindo porta...")
                    fila_porta.put(True)
                else:
                    print(cleaned_msg)
                full_msg = ''
                cleaned_msg = ''
                new_msg = True

        except:
            pass
        finally:
            cliente_ligado = recebe_mensagem_cliente(s, fila_mensagens)
    close_connection(s)


def recebe_mensagem_cliente(s, fila_mensagens):
    if (not fila_mensagens.empty()):
        msg = fila_mensagens.get()
        if (msg[0] == "envia img"):
            send_image(s, msg[1])
            return(True)
        elif (msg[0] == "envia log"):
            send_log(s, msg[1])
            return(True)
        elif (msg[0] == "cliente ligado"):
            return(msg[1])
    else:
        return(True)


def envia_data_encoding(s):
    dt = str(os.path.getmtime("encodings.pickle"))
    msg_dt = "enco dt:" + dt
    send_message(s, msg_dt)


def recebe_encoding(dados, fila_encodings):
    msg = conteudo_msg(dados)
    encodings = eval(msg)
    fila_encodings.put(encodings)
    with open("encodings.pickle", "wb") as f:
        f.write(encodings)
    print("Novos encodings recebidos.")


def conteudo_msg(msg):
    inicio = msg.find(":")+1
    return msg[inicio::]
