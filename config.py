"""
    配置文件
"""
import dotenv#
from pathlib import Path#
import os#
dotenv.load_dotenv(verbose=True)

#交易所 api配置
KP_EXCHANGE_CCXT = {
    'exchange' : 'okx',
    "apiKey" : os.getenv('okx_ro_apikey'),
    "secret" : os.getenv('okx_ro_secret'),
    "password" : os.getenv('okx_ro_password'),
    'timeout': 3000,
    # rateLimit = 2000,
    # milliseconds = seconds * 1000
    'enableRateLimit': True,
    'retry_max' : 3, #同一个请求发生错误重试三次
}

#存储类型: csv、questdb
KP_GLOBAL_DATABASE = {
    # 'type'   : 'questdb',
    'type'   : 'csv',
    'prefix' : 'kp_', #表or文件名前缀

    "host" : os.getenv('questdb_host'),
    "influxdb_port" : os.getenv('questdb_influxdb_port'),
    "health_port" :   os.getenv('questdb_health_port'),
}

#拉取标的配置
KP_GLOBAL_SYMBOLS = [
    {
        'symbol'   : 'ETH/USDT',
        'table'    : 'ohlcv_eth', #csv文件名 or qdb表名
    },
    {
        'symbol'   : 'ETH/USDT:USDT-221230',  #当季合约
        'table'    : 'ohlcv_cq'
    },
]
KP_GLOBAL_DATERANGE = {
    'timeframe': '1m', #1分钟数据
    'fromdate' : '2021-01-01 00:00:00', #开始时间
    'todate'   : '2022-09-01 00:00:00', #结束时间
    'limit'    : 100, #默认分页数
}
#END symbols

#合成基差率配置
KP_GLOBAL_BASIS = [
    {   
        'name'   : 'ETH_CQ_BASIS',  #基差率
        'formula': '100*({1}-{0})/{1}', #计算公式
        'table'  : 'ohlcv_cq_basis', 
    },
]
#END basis






