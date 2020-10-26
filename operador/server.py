import socket
import queue
import time
import select


def executa_servidor(servidor_ligado, fila_server, interface):
    try:
        HEADERSIZE = 10
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(False)
        s.bind((socket.gethostname(), 6418))
        s.listen(5)
        cliente_conectado = False

        while servidor_ligado:
            time.sleep(0.0125)
            try:
                clientsocket, address = s.accept()
                clientsocket.setblocking(False)
                print(f"Conexão com {address} foi estabelecida!")
                full_log = ''
                new_log = True
                cliente_conectado = True
            except:
                pass
            finally:
                pass

            while servidor_ligado and cliente_conectado:
                time.sleep(0.0125)
                try:
                    log = clientsocket.recv(32)
                    if new_log:
                        loglen = int(log[:HEADERSIZE])
                        new_log = False

                    full_log += log.decode("utf-8")
                    cleaned_log = full_log[HEADERSIZE:]

                    if (len(cleaned_log) == loglen) and (cleaned_log != "close conn"):
                        print("Log recebido!")
                        print(cleaned_log)
                        cleaned_log += '\n'
                        with open("logs.txt", "a") as f:
                            f.write(cleaned_log)
                        interface.atualizaLogs(cleaned_log)
                        full_log = ''
                        new_log = True

                    if cleaned_log == "close conn":
                        clientsocket.close()
                        print(f"Conexão com {address} foi encerrada!")
                        cliente_conectado = False
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


def fecha_conexao(s):
    s.close()
    print("Conexões encerradas.")


def recebe_sinal_servidor_ligado(fila_server):
    if (not fila_server.empty()):
        return(fila_server.get())
    else:
        return(True)
