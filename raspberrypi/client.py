import os.path
import socket
import time
import pickle
import ast

HEADERSIZE = 10


def cria_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_indisponivel = True
    contador = 0
    while server_indisponivel and contador <= 10:
        server_indisponivel = estabelece_conexao(s)
        contador += 1
        time.sleep(2)
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


def send_image(s):
    pass


def recv_message(cliente_ligado, fila_mensagens):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 6416))
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
                    recebe_encoding(cleaned_msg)
                elif cleaned_msg.startswith("enco dt:"):
                    envia_data_encoding(s)
                elif cleaned_msg.startswith("end con:"):
                    close_connection(s)
                else:
                    print(cleaned_msg)
                full_msg = ''
                cleaned_msg = ''
                new_msg = True

        except:
            pass
        finally:
            cliente_ligado = recebe_sinal_cliente_ligado(s, fila_mensagens)
    close_connection(s)


def recebe_sinal_cliente_ligado(s, fila_mensagens):
    if (not fila_mensagens.empty()):
        msg = fila_mensagens.get()
        if (msg[0] == "envia log"):
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


def recebe_encoding(dados):
    msg = conteudo_msg(dados)
    encodings = eval(msg)
    print("Novos encodings recebidos.")
    with open("encodings.pickle", "wb") as f:
        f.write(encodings)


def conteudo_msg(msg):
    inicio = msg.find(":")+1
    return msg[inicio::]
