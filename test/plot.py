"""
    根据数据画图
    
"""
import pandas as pd#
from  matplotlib import pyplot as plot#
import mplfinance as mpf#

file = 'kp_ohlcv_eth_cq_basis.csv'
df = pd.read_csv(file)

df['ts'] = pd.to_datetime(df['ts'])
df.set_index('ts',inplace=True)

mpf.plot(df2, type="candle", title="Candlestick for MSFT", ylabel="price($)")



print( df.head() )

