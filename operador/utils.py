
def nome_arquivo(caminho_arquivo):
    index_barra = caminho_arquivo[::-1].find('/')
    if index_barra == -1:
        return "Erro ao identificar caminho do arquivo."
    else:
        arquivo = caminho_arquivo[-index_barra::]
        return arquivo
