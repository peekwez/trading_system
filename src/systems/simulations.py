# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime as dt

# import database and system models
from data.models import DailyPrice, Symbol
from data.misc import colors
from data.plots import configure_plot, font_prop

# import panda and numpy libraries
import numpy as np
import pandas as pd

# import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rc, gridspec
from matplotlib.ticker import FuncFormatter, MaxNLocator


def smatrix(m,n,strategy):
    sig = np.zeros([m,n],dtype='object')
    for i in range(m):
        for k in range(n):
            action = strategy.get_signal()
            sig[i,k] =  strategy.get_signal()
    return sig

def plmatrix(signal,data):
    m,n = np.shape(signal)
    mat = np.zeros([m,n],dtype='float')
    for i in range(m):
        for k in range(n):
            action = signal[i,k]
            if action[0] != '':
                coeffs = action[1]
                mat[i,k] = coeffs[0]*data[k,0] + coeffs[1]*data[k,1]
    return mat

class MonteCarlo:
    """
    A monte-carlo simulation to test the random entry and exit
    """
    def __init__(self,strategy,ticker,capital=1000,size=100,sample=1000):
        self.strategy = strategy
        self.ticker = ticker
        self.size = size
        self.capital = capital
        self.nrows = sample

        # get dates
        self.end_date = '2014-12-31'
        self.start_date = '2014-01-01'

        # get prices
        self.symbol = Symbol.objects.get(ticker=ticker)
        self.set_prices()
        self.ncols = len(self.prices)

        # get signals
        self.set_signals()

    def set_signals(self):
        self.signals = smatrix(self.nrows,self.ncols,self.strategy)

    def set_win_loss(self):
        # get data and top 4 gainers and lowest  4 losers
        df = pd.DataFrame(data=self.sample_val,
                          index=[i for i in range(self.nrows)],
                          columns=['capital'])
        df_sort = df.sort_values(by='capital',ascending=False)
        heads = df_sort.head(4).index.values
        tails = df_sort.tail(4).index.values
        samples = np.concatenate((heads,tails))
        self.win_loss = samples

    def set_prices(self):
        tmp = DailyPrice.objects.filter(price_date__gte=self.start_date,
                                              price_date__lte=self.end_date,
                                              symbol__ticker=self.ticker,
                                          ).order_by('price_date').values_list(
                                              'open_price',
                                              'close_price',
                                              'price_date')
        self.prices  = np.array(tmp)

    def common_run(self):
        self.mat = plmatrix(self.signals, self.prices)
        self.daily_pl  = self.size*np.dot(self.mat,np.ones(self.ncols))
        self.sample_val = self.capital + self.daily_pl

    def backward_run(self):
        self.common_run()
        self.set_win_loss()
        self.plot(figname='backward')

    def forward_run(self):
        self.end_date = '2015-12-31'
        self.start_date = '2015-01-01'
        self.set_prices()
        self.prices = self.prices[:self.ncols]
        self.common_run()
        self.plot(figname='forward')

    def run_strategy(self):
        self.backward_run()
        self.forward_run()

    def plot(self,figname):

        # configure matplotlib
        configure_plot()

        # use colors for moving average chart
        colors = [colors.SYMB]
        ma_keys = ['MA_50', 'MA_10', 'MA_5', 'MA_40', 'MA_20', 'MA_30','MA_60']
        for key in ma_keys:
            colors.append(colors.MA[key])


        dates = self.prices[:,2]
        fig = plt.figure(figname + self.ticker, figsize=(11,7))
        gs  = gridspec.GridSpec(1,1)
        self.ax = fig.add_subplot(gs[0])

        for i,k in enumerate(self.win_loss):
            # slice sample of interest
            data = self.size*(self.mat[k,:])
            wins = np.sum(data > 0)
            loss = np.sum(data < 0)

            # accumulate gains and losses
            tmp = self.capital
            pl = np.zeros(self.ncols)
            for j,value in enumerate(data):
                tmp += float(value)
                pl[j] = tmp

            # get time series data
            ts = pd.Series(data=pl,index=dates)

            # plot time series
            ts.plot(ax=self.ax,color=colors[i], label='W={0:3d} L={1:3d}'.format(wins,loss))



        # set title
        self.ax.set_title('Random (Coin Toss) Trading Strategy for {0:s} - {1:s} Testing'.format(
            self.symbol.yahoo_ticker,
            figname.capitalize(),
        ),fontproperties=font_prop, size=13)

        # set axis labels
        self.ax.set_xlabel('Date', fontproperties=font_prop, size=13)
        self.ax.set_ylabel('Capital ({0:s})'.format(self.symbol.currency),
                           fontproperties=font_prop, size=13)

        # set tick label font
        plt.xticks(rotation=75)
        for label in self.ax.get_xticklabels():
            label.set_fontproperties(font_prop)
        self.ax.set_yticklabels(self.ax.get_yticks(), fontproperties=font_prop)

        # add legend
        legs = self.ax.legend(frameon=False, fontsize=13, loc='best', prop=font_prop)
        handles = legs.legendHandles
        for k, handle in enumerate(handles):
            handles[k].set_linewidth(4.0)

        # turn on grid
        self.ax.xaxis.grid()
        self.ax.yaxis.grid()

        # formatter for x- and y-axes
        ax_yfmt = FuncFormatter(lambda x, pos: '{0:d}'.format(int(x)))
        self.ax.yaxis.set_major_formatter(ax_yfmt)
