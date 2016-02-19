# -*- coding: utf-8 -*-
from __future__ import absolute_import


# import panda and matplotlib libraries
import pandas as pd

# import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rc, gridspec
from matplotlib.ticker import FuncFormatter, MaxNLocator

# import some math libraries
from math import floor, ceil

# import database models
from data.misc import colors
from data.models import DailyPrice, Symbol

# matplotlib settings
def configure_plot():
    if mpl.get_backend().lower() not in ['qt5agg', 'dt4agg', 'tkagg']:
        mpl.use("TKagg")
    mpl.rcParams['ps.usedistiller']  = 'xpdf'
    mpl.rcParams['ps.distiller.res'] = 6000
    font_prop.set_size(11)
    font_prop.set_weight(200)
    rc('legend', labelspacing=0.2, handleheight=1.)
    rc('savefig', format='pdf', dpi='400')
    rc('pdf', fonttype=3)
font_prop = fm.FontProperties(fname="monaco.ttf")

# plot function
class PlotSymbol:

    configure_plot()

    '''
    Plots figures for key, start and end dates specified
    for the tickers passed to the class.

    '''

    def __init__(self, tickers=['AAPL']):

        # initialized tickers, symbols and prices
        self.tickers = tickers
        self.nr_tickers = len(tickers)
        self.symbols = Symbol.objects.filter(ticker__in=tickers)
        self.prices = DailyPrice.objects.select_related('symbol').filter(
            symbol__ticker__in=tickers)


    def plot(self, key='close_price', ma_type='simple', start_date='', end_date=''):

        # build kwargs
        kwargs = {}
        if start_date != '': kwargs['price_date__gte'] = start_date
        if end_date   != '': kwargs['price_date__lte'] = end_date

        # loop through all tickers
        for ticker in self.tickers:
            self.__plot(key, ticker, ma_type, **kwargs)

    def __plot(self, key, ticker, ma_type, **kwargs):

        # get prices, symbol and company name
        prices = self.prices.filter(symbol__ticker=ticker,**kwargs).order_by('price_date').values()
        symbol = self.symbols.get(ticker=ticker)
        company = symbol.name
        yahoo_ticker = symbol.yahoo_ticker
        currency = symbol.currency

        # create panda data frame and time series
        df = pd.DataFrame.from_records(prices)
        ts = pd.Series([float(x) for x in df[key]], index=df['price_date'])
        vs = pd.Series([float(x) for x in df['volume']], index=df['price_date'])


        # get figures and sizes
        fig = plt.figure(yahoo_ticker+ma_type, figsize=(11,10))
        gs  = gridspec.GridSpec(2,1, height_ratios=[5,3])
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])


        # ADD SUBPLOT FOR KEY
        # ====================

        # plot values for key
        ts.plot(ax=ax1, color=colors.SYMB, legend=True, label='{0:s}'.format(yahoo_ticker))

        # add fill to plot
        ax1.fill_between(ts.index, ts.values, facecolor=colors.FILL, alpha=0.9)


        # add moving averages
        ma_keys = ['MA_5', 'MA_10', 'MA_20', 'MA_30', 'MA_40', 'MA_50', 'MA_60']
        len_ma = len(ma_keys)
        for k in range(len_ma):
            ma   = ma_keys[k]
            tmp  = ma.split('_')
            days = int(tmp[1])
            end_label = ' '.join(word for word in tmp)

            # plot simple moving average
            if ma_type == 'simple':
                label = 'S' + end_label
                pd.rolling_mean(ts,days).plot(ax=ax1,
                                              color=colors.MA[ma],
                                              legend=True,
                                              label=label)
            elif ma_type == 'exponential':
                label = 'E' + end_label
                pd.ewma(ts,span=days).plot(ax=ax1,
                                           color=colors.MA[ma],
                                           legend=True,
                                           label=label)

        # function for y label name
        name = lambda w: ' '.join(word.capitalize() for word in w.split('_'))

        # set axis labels
        ax1.set_xlabel('Date', fontproperties=font_prop, size=13)
        ax1.set_ylabel('{0:s} ({1:s})'.format(name(key), currency), fontproperties=font_prop, size=13)

        # set axis ticks
        plt.setp(ax1.get_xticklabels(), visible=False)
        ax1.set_yticklabels(ax1.get_yticks(), fontproperties=font_prop)

        # turn grid on
        ax1.xaxis.grid()
        ax1.yaxis.grid()

        # formatter for y-axis
        ax1_yfmt = FuncFormatter(lambda x, pos: '{0:g}'.format(x/1.))
        ax1.yaxis.set_major_formatter(ax1_yfmt)

        # set limits for y-axis
        ymax = ts.max()
        ymin = ts.min()
        ax1.set_ylim([floor(ymin), max(ymax, floor(ymax)+0.5)])

        # get plot end values and add legends
        legs = ax1.legend(frameon=False, fontsize=13, loc='best', prop=font_prop)
        lines = ax1.lines

        texts = legs.get_texts()
        handles = legs.legendHandles
        for k, line in enumerate(lines):
            value = line.get_ydata()[-1]
            text  = texts[k].get_text()
            label = '{0:6s} - {1:0.2f} {2:s}'.format(text,value,currency)

            # set new values and labels
            handles[k].set_linewidth(4.0)
            texts[k].set_text(label)

        # add title for this plot
        ax1.set_title(
            '{0:s} ({1:s}) from {2:s} to {3:s}'.format(company,
                                                       yahoo_ticker,
                                                       kwargs['price_date__gte'],
                                                       kwargs['price_date__lte']),
            fontproperties=font_prop, size=13)

        # ADD SUBPLOT OF VOLUME TRADED
        # ============================

        # plot vertical lines for volume
        ax2.vlines(vs.index, [0], vs.values, color=colors.VLINE)

        # set axis labels
        ax2.set_xlabel('Date', fontproperties=font_prop, size=13)
        ax2.set_ylabel('Volume (in 1000 stocks)', fontproperties=font_prop, size=13)

        # set axis ticks
        plt.xticks(rotation=75)
        for label in ax2.get_xticklabels():
            label.set_fontproperties(font_prop)
        ax2.set_yticklabels(ax2.get_yticks(), fontproperties=font_prop)

        # turn on grid
        ax2.xaxis.grid()
        ax2.yaxis.grid()

        # formatter for y-axis
        ax2_yfmt = FuncFormatter(lambda x, pos: '{0:g}'.format(x/1000))
        ax2.yaxis.set_major_formatter(ax2_yfmt)
        ax2.yaxis.set_major_locator(MaxNLocator(prune='upper')) # remove last tick label

        # remove horizontal space between subplots
        fig.subplots_adjust(hspace=0.001)
