"""
    配置文件
"""

KP_GLOBAL_DATABASE = {
    'type'   : 'csv',
    'prefix' : 'kp_', #表or文件名前缀
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
    'fromdate' : '2020-01-01 00:00:00', #开始时间
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



