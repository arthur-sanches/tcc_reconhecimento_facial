import os.path
import socket
import queue
import time
import select
import pickle

HEADERSIZE = 10


def executa_servidor(servidor_ligado, fila_server, fila_encoding, fila_porta, interface):
    servidor_ligado = True
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(False)
        s.bind(("192.168.15.13", 6416))
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
                        if cleaned_msg.startswith("new img:"):
                            recebe_frame(cleaned_msg, interface)
                        elif cleaned_msg.startswith("new log:"):
                            receive_log(cleaned_msg, interface)
                        elif cleaned_msg.startswith("enco dt:"):
                            data_enc_cliente = recebe_data_encoding(
                                cleaned_msg)
                            data_enc_local = os.path.getmtime(
                                "encodings.pickle")
                            if data_enc_local > data_enc_cliente:
                                envia_encoding(clientsocket)
                        else:
                            print(cleaned_msg)
                        full_msg = ''
                        cleaned_msg = ''
                        new_msg = True

                except:
                    pass
                finally:
                    servidor_ligado = recebe_sinal_servidor_ligado(fila_server)
                    if recebe_sinal_encoding(fila_encoding):
                        print("Requisitando data dos Encodings...")
                        pede_dt_enc_cliente(clientsocket)
                    recebe_sinal_porta(clientsocket, fila_porta)

            if servidor_ligado:
                servidor_ligado = recebe_sinal_servidor_ligado(fila_server)
    except:
        pass
    finally:
        fecha_conexao(s)
        print("Servidor desligado.")


def envia_mensagem(s, msg):
    msg = f"{len(msg):<{HEADERSIZE}}" + msg
    try:
        s.send(bytes(msg, "utf-8"))
        print("Mensagem enviada com sucesso!")
    except:
        print("Falha ao enviar mensagem.")
    finally:
        pass


def envia_encoding(s):
    with open("encodings.pickle", "rb") as f:
        dados = f.read()
    encodings = str(dados)
    msg = "new enc:" + encodings
    envia_mensagem(s, msg)
    print("Arquivo encodings.pickle enviado!")


def pede_dt_enc_cliente(s):
    msg = "enco dt:"
    envia_mensagem(s, msg)


def recebe_frame(msg, interface):
    frame_msg = conteudo_msg(msg)
    frame_bytes = eval(frame_msg)
    interface.atualizaFrame(frame_bytes)


def receive_log(msg, interface):
    log = conteudo_msg(msg)
    print(f"Novo acesso: {log}")
    log += '\n'
    with open("logs.txt", "a") as f:
        f.write(log)
    interface.atualizaLogs(log)


def recebe_data_encoding(msg):
    data = conteudo_msg(msg)
    return float(data)


def fecha_conexao(s):
    envia_mensagem(s, 'end con:')
    s.close()
    print("Conexões encerradas.")


def recebe_sinal_encoding(fila_encoding):
    if (not fila_encoding.empty()):
        return(fila_encoding.get())
    else:
        return(False)


def recebe_sinal_servidor_ligado(fila_server):
    if (not fila_server.empty()):
        return(fila_server.get())
    else:
        return(True)


def recebe_sinal_porta(s, fila_porta):
    if (not fila_porta.empty()):
        sinal = fila_porta.get()
        if sinal == True:
            envia_mensagem(s, 'abr prt:')


def conteudo_msg(msg):
    inicio = msg.find(":")+1
    return msg[inicio::]
