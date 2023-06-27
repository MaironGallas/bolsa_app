from datetime import datetime, timedelta, time
from datetime import datetime, time
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import seaborn as sns
import MetaTrader5 as mt5
from time import sleep


class GraphRealTime():
    def __init__(self, df_passado):
        self.df = df_passado


class Analise():
    def __init__(self, ):
        pass

    def filter_time_frame(self, dict_dolar):

        style = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 6})
        df_tt_dolar = pd.DataFrame(dict_dolar)
        df_tt_dolar['Hora'] = pd.to_datetime(df_tt_dolar.Hora)
        df_tt_dolar = df_tt_dolar.set_index('Hora')

        ohlc_data = df_tt_dolar.resample('2min').agg({'Preço': ['first', 'max', 'min', 'last']})

        ohlc_data.columns = ['open', 'high', 'low', 'close']

        if hasattr(self, 'fig'):
            self.ax.clear()
            mpf.plot(ohlc_data, type='candle', ax=self.ax, style=style)

        else:
            self.fig, ax = mpf.plot(ohlc_data, type='candle', style=style, returnfig=True)
            self.ax = ax[0]

        plt.show()
        plt.pause(0.001)

    def make_correlation(self):
        # Defina a janela atual de 2 minutos.

        # Conectar ao MetaTrader 5
        if not mt5.initialize():
            print("Falha ao conectar ao MetaTrader 5!")
            quit()

        # Definir os ativos para monitorar
        # symbols = ['MinDolMar23', 'Usa500', 'Bra50']
        symbols = ['USDJPY', 'GBPUSD', 'Usa500']

        # Definir a duração da coleta de dados (em segundos)
        duration = 60  # 1 minuto

        # Definir o intervalo de tempo para cada coleta de dados (em segundos)
        interval = 1  # 1 segundo

        # Definir o DataFrame para armazenar os valores calculados
        data = pd.DataFrame(columns=symbols)

        # Coletar 60 valores por 1 minuto
        for i in range(duration * interval):
            # Obter o último tick para cada símbolo
            for symbol in symbols:
                tick = mt5.symbol_info_tick(symbol)
                if tick is not None:
                    # Obter a barra anterior para cada símbolo
                    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, 2)
                    pd_rates = pd.DataFrame(rates)
                    if rates is not None and len(rates) > 1:
                        current_price = pd_rates.close[1]
                        previous_close = pd_rates.close[0]
                        if previous_close != 0:
                            tick_change = (current_price - previous_close) / previous_close * 100
                            time1 = datetime.now().time()
                            data.loc[i, symbol] = tick_change
            # Aguardar um segundo antes da próxima coleta de dados
            sleep(interval)

        data = data.astype(float)
        # data['time'] = time
        # data = data.set_index('time')
        correlation = data.corr()

        print(datetime.now().time())

        """if hasattr(self, 'fig_warm'):
            self.ax_warm.clear()
            sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=self.ax_warm, cbar=False)
            cbar = self.ax.figure.colorbar(self.ax.collections[0])
        else:
            self.fig_warm, self.ax_warm = plt.subplots()
            sns.heatmap(correlation, annot=True, cmap='coolwarm', cbar=True)

        plt.show()
        plt.pause(0.001)"""

        # Zerar o DataFrame
        data = pd.DataFrame(columns=symbols, index=pd.DatetimeIndex([], name='time'))


