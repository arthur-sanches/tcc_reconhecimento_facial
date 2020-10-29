import socket
import queue
import time
import select


def executa_servidor(servidor_ligado, fila_server, interface):
    try:
        HEADERSIZE = 10
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(False)
        s.bind((socket.gethostname(), 6416))
        s.listen(5)
        cliente_conectado = False

        while servidor_ligado:
            time.sleep(0.01)
            try:
                clientsocket, address = s.accept()
                clientsocket.setblocking(False)
                print(f"Conexão com {address} foi estabelecida!")
                full_msg = ''
                new_msg = True
                cliente_conectado = True
            except:
                pass
            finally:
                pass

            while servidor_ligado and cliente_conectado:
                time.sleep(0.01)
                try:
                    msg = clientsocket.recv(4096)
                    if new_msg:
                        msg_len = int(msg[:HEADERSIZE])
                        new_msg = False

                    full_msg += msg.decode("utf-8")
                    cleaned_msg = full_msg[HEADERSIZE:]
                    if cleaned_msg == "close conn":
                        clientsocket.close()
                        print(f"Conexão com {address} foi encerrada!")
                        cliente_conectado = False
                    elif (len(cleaned_msg) == msg_len):
                        print("Mensagem recebido!")
                        if cleaned_msg.startswith("new log:"):
                            receive_log(cleaned_msg, interface)
                        elif cleaned_msg.startswith("enco dt:"):
                            send_encoding(cleaned_msg, interface, HEADERSIZE)
                        full_msg = ''
                        new_msg = True

                except:
                    pass
                finally:
                    servidor_ligado = recebe_sinal_servidor_ligado(fila_server)

            if servidor_ligado:
                servidor_ligado = recebe_sinal_servidor_ligado(fila_server)
    except:
        pass
    finally:
        fecha_conexao(s)
        print("Servidor desligado.")


def receive_log(msg, interface):
    log = conteudo_msg(msg)
    print(f"Novo acesso: {log}")
    log += '\n'
    with open("logs.txt", "a") as f:
        f.write(log)
    interface.atualizaLogs(log)


def send_encoding(msg, interface, HEADERSIZE):
    encoding_date_rasp = int(conteudo_msg(msg))
    if interface.encoding_date > encoding_date_rasp:
        with open("encodings.pickle", "rb") as f:
            encodings = f.read()
        header_msg = f"{len(encodings):<{HEADERSIZE}}new enc:".encode
        b"" + header_msg + encodings
        # clientsocket.send(encodings)


def fecha_conexao(s):
    s.close()
    print("Conexões encerradas.")


def recebe_sinal_servidor_ligado(fila_server):
    if (not fila_server.empty()):
        return(fila_server.get())
    else:
        return(True)


def conteudo_msg(msg):
    inicio = msg.find(":")+1
    return msg[inicio::]
