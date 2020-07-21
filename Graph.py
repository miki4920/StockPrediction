import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import MONDAY
import mplfinance as mpf


class Graph(object):
    def __init__(self, stock_name, data):
        # Imports a style
        plt.style.use("seaborn")
        # Creates an axis
        self.axis = plt.subplot2grid((1, 1), (0, 0))
        self.axis.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.months = mdates.MonthLocator(range(1, 13), bymonthday=1, interval=1)
        # Sets ticks
        self.axis.xaxis.set_major_locator(self.months)

        # Creates variables to store data
        self.stock_name = stock_name
        self.data = data
        self.date = []

    def linear_graph(self):
        # Iterates through data columns
        for column in self.data:
            # Plots each column, creating a legend 0as well
            plt.plot_date(self.data.index, self.data[column], "-", label=column)

    def candle_graph(self):
        # Creates a candlestick graph
        mc = mpf.make_marketcolors(up='g', down='r')
        s = mpf.make_mpf_style(marketcolors=mc)
        mpf.plot(self.data, type="candle", style=s, title=self.stock_name, ylabel='OHLC Candles')

    def bar_graph(self):
        # Create bars with low and high prices,
        plt.bar(self.data.index, 10, width=1, bottom=self.data['High'].apply(lambda x: x-10), label='High')
        plt.bar(self.data.index, 10, width=1, bottom=self.data['Low'].apply(lambda x: x-10), label='Low')

    def area_graph(self):
        plt.fill_between(self.data.index, self.data['High'], self.data['Low'], label="High-Low")

    def scatter_graph(self):
        for column in self.data:
            plt.scatter(self.data.index, self.data[column], s=2, label=column)

    def start_graph(self):
        for label in self.axis.xaxis.get_ticklabels():
            label.set_rotation(45)
        # Scales the window
        self.axis.autoscale_view()
        # Sets a grid up
        self.axis.grid(True)
        # Sets up legend
        plt.legend()
        # Creates a title for the graph
        plt.title(self.stock_name)
        # Opens the graph window
        plt.show()
