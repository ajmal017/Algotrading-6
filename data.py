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




class IBDataHandler(DataHandler):
	"""
	Utilizes ib_insync API to handle interactive brokers data
	"""

	def __init__(self, events, ib, symbol_list):
        """
        Initialises the historic data handler by requesting
        an IB object and a list of symbols.

        Parameters:
        events - The Event Queue.
        ib - Interactive Brokers connection
        symbol_list - A list of symbol strings.
        """
        self.events = events
        self.ib = ib
        self.symbol_list = symbol_list

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Fix this
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


