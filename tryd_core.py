import pandas as pd
import socket
import numpy as np
from collections import deque


class SocketTryd():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.parar = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conectado = False

    def conectar(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.parar = True
        except Exception as ex:
            print(ex)

    def desconectar(self):
        self.socket.close()
        self.conectado = False
        self.parar = False

    def is_conexao_estabelecida(self):
        if self.socket is not None:
            try:
                self.socket.getpeername()
                self.conectado = True
                return self.conectado

            except OSError:
                self.conectado = False
                return self.conectado
        else:
            self.conectado = False
            return self.conectado


class BookFechado():
    def __init__(self, host='127.0.0.1', port=12002, ativo='DOLJ23'):
        self.socket_tryd = SocketTryd(host, port)
        self.ativo = ativo
        self.df_book_fechado = pd.DataFrame(columns=['OftC', 'QtdC', 'Cpa', 'Vda', 'QtdV', 'OftV'])
        self.linhas = 5
        self.colunas = 6

    def coletar_dados(self):
        data = b''

        while self.socket_tryd.parar:
            try:
                for linha in range(0, self.linhas):
                    for coluna in range(0, self.colunas):
                        self.socket_tryd.socket.sendall(str.encode('LVL2$S|' + '1|' + self.ativo + '|' + str(linha) + '|' + str(coluna) + '|#'))

                chunk = self.socket_tryd.socket.recv(8192)
                if len(chunk) >= 8192:
                    data = data + chunk
                else:
                    data = data + chunk

                    self.processa_dados(data)

                    data = b''

            except Exception as ex:
                print(f'Não foi possivel enviar msg, Erro: {ex}')

    def processa_dados(self, dados):
        matriz_np_book = np.empty((self.linhas, self.colunas))

        data = dados
        itens = data.decode("utf-8").replace("LVL2!", "").replace("#", "").split('|')
        for item in itens:
            a = item.split(";")
            if len(a) > 1:
                matriz_np_book[int(a[1])][int(a[2])] = a[3].replace(",", ".")

        self.df_book_fechado = pd.DataFrame(matriz_np_book, columns=['OftC', 'QtdC', 'Cpa', 'Vda', 'QtdV', 'OftV'])


class TimesAndTrades():
    def __init__(self, host='127.0.0.1', port=12002, ativo='DOLJ23'):
        self.socket_tryd = SocketTryd(host, port)
        self.ativo = ativo
        self.ultimo_preco = 999
        self.times_dict = {"Hora": [], "Qtd": [], "Preço": [], "CC": [], "CV": [], "Agr": []}

    def coletar_dados(self):
        data = b''
        while self.socket_tryd.parar:
            try:
                self.socket_tryd.socket.sendall(str.encode('NEGS$S|' + self.ativo + '#'))
                chunk = self.socket_tryd.socket.recv(8192)
                if len(chunk) >= 8192:
                    data = data + chunk
                else:
                    data = data + chunk

                    self.processa_dados(data)

                    data = b''

            except Exception as ex:
                print(f'Não foi possivel enviar msg, Erro: {ex}')

    def processa_dados(self, dados):
        fila_desvio_padrao = deque(maxlen=30)

        data = dados
        itens = data.decode().split("|")

        if len(itens) == 8 and itens[1].find('@') == -1:
            new_data = {'Hora': itens[2], 'Qtd': int(itens[4]), 'Preço': float(itens[3].replace('.', '').replace(',', '.')), 'CC': int(itens[5]), 'CV': int(itens[6]), 'Agr': itens[7].replace('#', "")}
            for chave, valor in new_data.items():
                self.times_dict[chave].append(valor)

        else:
            hora = itens[2].split('@')
            qtd = itens[4].split('@')
            preco = itens[3].split('@')
            cc = itens[5].split('@')
            cv = itens[6].split('@')
            agr = itens[7].split('@')

            for i in range(len(hora)):
                new_data = {'Hora': hora[i], 'Qtd': int(qtd[i]), 'Preço': float(preco[i].replace('.', '').replace(',', '.')), 'CC': int(cc[i]), 'CV': int(cv[i]), 'Agr': agr[i].replace('#', "")}
                for chave, valor in new_data.items():
                    self.times_dict[chave].append(valor)


        """ultimos_30_trades_preco = self.times_dict['Preço'][-30:]
        ultimos_30_trades_hora = self.times_dict['Hora'][-30:]

        if self.ultimo_preco == 999:
            self.ultimo_preco = ultimos_30_trades_preco[-1]
            self.ultima_hora = ultimos_30_trades_hora[-1]
        else:
            deslocamento_preco = ultimos_30_trades_preco[-1] - self.ultimo_preco
            deslocamento_hora = ultimos_30_trades_hora[-1] - self.ultima_hora

            self.ultimo_preco = ultimos_30_trades_preco[-1]
            self.ultima_hora = ultimos_30_trades_hora[-1]

            #print(deslocamento_hora)
            #print(deslocamento_preco)"""

        """fila_desvio_padrao.append(abs(df_ultimos_30_trades.iloc[-1]['Preço'] - df_ultimos_30_trades.iloc[0]['Preço']))
        if len(fila_desvio_padrao) == 30:
            desvio_padrao = statistics.stdev(fila_desvio_padrao)
            print(f"Desvio padrão: {desvio_padrao:.2f}")

        print(df_ultimos_30_trades.iloc[-1]['Hora'] - df_ultimos_30_trades.iloc[0]['Hora'])
        print(df_ultimos_30_trades.iloc[-1]['Preço'] - df_ultimos_30_trades.iloc[0]['Preço'])"""
