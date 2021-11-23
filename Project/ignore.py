import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import yfinance as yf
import html5lib
major_indices = pd.read_html("https://www.cboe.com/us/equities/market_statistics/listed_symbols/")[0]
ticker_list= major_indices['Symbol'].to_list()
print(ticker_list)
