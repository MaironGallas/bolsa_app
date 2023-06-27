import sys
import os

from analise_core import Analise
from qt_core import *
import pandas as pd
import numpy as np
from gui.windows.main_window.ui_main_window import *
import threading
from tryd_core import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = UiMainWindow()
        self.ui.setup_ui(self)

        # Toggle button
        self.ui.toggle_button.clicked.connect(self.toggle_button)

        # Btn home
        self.ui.btn_1.clicked.connect(self.show_page_1)

        # Btn widgets
        self.ui.btn_2.clicked.connect(self.show_page_2)

        # Btn widgets
        self.ui.btn_3.clicked.connect(self.conectar)

        # Btn widgets
        self.ui.btn_4.clicked.connect(self.desconectar)

        # Btn widgets
        self.ui.settings_btn.clicked.connect(self.show_page_3)

        self.trades_indice = TimesAndTrades(host='127.0.0.1', port=12002, ativo='WINJ23')
        self.trades = TimesAndTrades(host='127.0.0.1', port=12002, ativo='DOLK23')

        self.book_fechado = BookFechado()
        self.analise = Analise()

        # Somente Adicionar Objetos que são linkados ao tryd.
        self.lista_tryd = [self.trades, self.book_fechado, self.trades_indice]

        """self.temporizador_2 = QTimer()
        self.temporizador_2.timeout.connect(self.update_corre)
        self.temporizador_2.start(60020)"""

        self.show()

    def update_corre(self):
        #self.analise.filter_time_frame(self.trades.times_dict)
        self.analise.make_correlation()

    def update_table_book_fechado(self):
        num_linhas = len(self.book_fechado.df_book_fechado)
        num_colunas = len(self.book_fechado.df_book_fechado.columns)
        self.ui.ui_pages.table_book.setHorizontalHeaderLabels(self.book_fechado.df_book_fechado.columns)

        self.ui.ui_pages.table_book.setRowCount(num_linhas)
        self.ui.ui_pages.table_book.setColumnCount(num_colunas)

        for i in range(num_linhas):
            for j in range(num_colunas):
                item = QTableWidgetItem(str(self.book_fechado.df_book_fechado.iloc[i, j]))
                item.setTextAlignment(Qt.AlignCenter)

                self.ui.ui_pages.table_book.setItem(i, j, item)

        self.ui.ui_pages.table_book.setColumnWidth(0, 60)  # 100 pixels para a primeira coluna
        self.ui.ui_pages.table_book.setColumnWidth(1, 65)  # 150 pixels para a segunda coluna
        self.ui.ui_pages.table_book.setColumnWidth(2, 65)  # 200 pixels para a terceira coluna
        self.ui.ui_pages.table_book.setColumnWidth(3, 55)  # 200 pixels para a terceira coluna
        self.ui.ui_pages.table_book.setColumnWidth(4, 55)  # 200 pixels para a terceira coluna
        self.ui.ui_pages.table_book.setColumnWidth(5, 100)  # 200 pixels para a terceira coluna

    def update_table_times(self):
        ultimos_50_itens = {}

        for chave in self.trades_indice.times_dict:
            ultimos_50_itens[chave] = self.trades_indice.times_dict[chave][-50:]

        num_linhas = len(ultimos_50_itens["Preço"])
        num_colunas = len(ultimos_50_itens)
        self.ui.ui_pages.table_times.setHorizontalHeaderLabels(ultimos_50_itens.keys())

        self.ui.ui_pages.table_times.setRowCount(num_linhas)
        self.ui.ui_pages.table_times.setColumnCount(num_colunas)

        for linha in range(num_linhas):
            for coluna in range(num_colunas):
                if coluna == 0:
                    item = QTableWidgetItem(str(list(ultimos_50_itens.values())[coluna][linha]))
                else:
                    item = QTableWidgetItem(str(list(ultimos_50_itens.values())[coluna][linha]))

                item.setTextAlignment(Qt.AlignCenter)

                if coluna == 5 and list(ultimos_50_itens.values())[coluna][linha] == "Vendedor":
                    item.setBackground(QColor(255, 0, 0, 120))  # Vermelho semi-transparente
                elif coluna == 5 and list(ultimos_50_itens.values())[coluna][linha] == "Comprador":
                    item.setBackground(QColor(0, 255, 0, 120))  # Vermelho semi-transparente

                self.ui.ui_pages.table_times.setItem(linha, coluna, item)

        self.ui.ui_pages.table_times.setColumnWidth(0, 60)  # 100 pixels para a primeira coluna
        self.ui.ui_pages.table_times.setColumnWidth(1, 65)  # 150 pixels para a segunda coluna
        self.ui.ui_pages.table_times.setColumnWidth(2, 65)  # 200 pixels para a terceira coluna
        self.ui.ui_pages.table_times.setColumnWidth(3, 55)  # 200 pixels para a terceira coluna
        self.ui.ui_pages.table_times.setColumnWidth(4, 55)  # 200 pixels para a terceira coluna
        self.ui.ui_pages.table_times.setColumnWidth(5, 100)  # 200 pixels para a terceira coluna

    # Toggle button
    def toggle_button(self):
        # Get menu width
        menu_width = self.ui.left_menu.width()

        # Check with
        width = 50
        if menu_width == 50:
            width = 240

        # Start animation
        self.animation = QPropertyAnimation(self.ui.left_menu, b"minimumWidth")
        self.animation.setStartValue(menu_width)
        self.animation.setEndValue(width)
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutCirc)
        self.animation.start()

    # Btn widgets function
    def show_page_1(self):
        self.reset_selection()
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.page_1)
        self.ui.btn_1.set_active(True)

    # Btn widgets function
    def show_page_2(self):
        self.reset_selection()
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.page_2)
        self.ui.btn_2.set_active(True)

    # Btn widgets function
    def conectar(self):
        #self.reset_selection()
        self.lista_thread = []

        for obj in self.lista_tryd:
            obj.socket_tryd.conectar()
            if obj.socket_tryd.is_conexao_estabelecida():
                self.ui.bottom_label_left.setText('Status: Conectado')
                self.lista_thread.append(threading.Thread(target=obj.coletar_dados))

        for thread in self.lista_thread:
            thread.start()

        self.temporizador = QTimer()
        self.temporizador.timeout.connect(self.update_table_times)
        self.temporizador.timeout.connect(self.update_table_book_fechado)
        self.temporizador.start(200)

    def desconectar(self):
        # self.reset_selection()
        self.ui.bottom_label_left.setText('Status: Desconectado')
        for obj in self.lista_tryd:
            obj.socket_tryd.desconectar()

        for thread in self.lista_thread:
            thread.join()

        self.temporizador.stop()
        #self.ui.btn_3.set_active(True)

    # Btn pase gettings
    def show_page_3(self):
        self.reset_selection()
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.page_3)
        self.ui.settings_btn.set_active(True)

    # Reset BTN Selection
    def reset_selection(self):
        for btn in self.ui.left_menu.findChildren(QPushButton):
            try:
                btn.set_active(False)
            except:
                pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.aboutToQuit.connect(window.desconectar)
    sys.exit(app.exec())
