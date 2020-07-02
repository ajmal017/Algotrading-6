# Imports
import datetime
import os, os.path
import pandas as pd

from abc import ABCMeta, abstractmethod

from event import MarketEvent


class DataHandler(object):
    """
    DataHandler is an abstract base class providing an interface for
    all subsequent (inherited) data handlers (both live and historic).

    The goal of a (derived) DataHandler object is to output a generated
    set of bars (OLHCVI) for each symbol requested. 

    This will replicate how a live strategy would function as current
    market data would be sent "down the pipe". Thus a historic and live
    system will be treated identically by the rest of the backtesting suite.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_latest_bars(self, symbol, N=1):
        """
        Returns the last N bars from the latest_symbol list,
        or fewer if less bars are available.
        """
        raise NotImplementedError("Should implement get_latest_bars()")

    
    @abstractmethod
    def update_bars(self):
        """
        Pushes the latest bar to the latest symbol structure
        for all symbols in the symbol list.
        """
        raise NotImplementedError("Should implement update_bars()")




class BacktestAlpacaDataHandler(DataHandler):
	"""
	Utilizes Alpaca API to handle interactive brokers data
	"""

	def __init__(self, events, alpaca, symbol_list,start,end):
        """
        Initialises the historic data handler by requesting
        an IB object and a list of symbols.

        Parameters:
        events - The Event Queue.
        ib - Interactive Brokers connection
        symbol_list - A list of symbol strings.
        """
        self.events = events
        self.alpaca = alpaca
        self.symbol_list = symbol_list
        self.start = start
        self.end = end

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True

        self.get_alpaca_data()

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Fix this
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # quantopian/zipline "pipeline" data structure ff

    def get_alpaca_data(self):
        """
        Gets requested data from Alpaca API
        
        """

        data = pd.DataFrame()
        for t in self.symbol_list:
            bars = self.alpaca.polygon.historic_agg_v2(t, 1, 'day', _from = self.start, to = self.end).df
            bars['name'] = t
            data = data.append(bars)

        data.reset_index(inplace=True)
        data.set_index(['timestamp', 'name'], inplace=True)
        data.sort_index(inplace=True)


    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # plz fix
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def _get_new_bar(self, symbol):
        """
        Returns the latest bar from the data feed 
        """
        for date in self.symbol_data.index.get_level_values('date').unique():
            yield symbol_data.loc[index]


    def get_latest_bars(self, symbol, N=1):
        """
        Returns the last N bars from the latest_symbol list,
        or N-k if less available.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print "That symbol is not available in the historical data set."
        else:
            return bars_list[-N:]

    def update_bars(self):
        """
        Pushes the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        for s in self.symbol_list:
            try:
                bar = self._get_new_bar(s).next()
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[s].append(bar)
        self.events.put(MarketEvent())


