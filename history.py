"""
    拉取历史ohlcv数据
"""
from time import sleep#
from urllib import request#
from datetime import datetime

from loguru import logger#
import ccxt#
try:
    import questdb.ingress#
    # from questdb.ingress import Sender, IngressError,TimestampNanos
except ImportError:
    print("use questdb with pip install questdb")

from config import KP_GLOBAL_DATABASE#存储
from config import KP_GLOBAL_DATERANGE#时间区间
from config import KP_GLOBAL_BASIS#基差率
from config import KP_GLOBAL_SYMBOLS#标的
from config import KP_EXCHANGE_CCXT#交易所信息


class kp_history():
    
    kp_exchange = None
    kp_datebase = None
    
    
    def __init__(self) -> None:
        """
        1、交易所 time check
        2、数据库 health check
        """
        logger.add('runtime.log', backtrace=True, diagnose=True, rotation='00:00', retention='1 week')
        
        exchange_class = getattr(ccxt,KP_EXCHANGE_CCXT['exchange'])
        self.kp_exchange = exchange_class(KP_EXCHANGE_CCXT)
        
        # self.check_exchange_time()
        self.check_database_health()
        
    #END __init__

    def run(self,):
        self.pull_candles()
        

    def pull_candles(self,):
        while_condition = True
        
        timeframe = KP_GLOBAL_DATERANGE['timeframe'] if KP_GLOBAL_DATERANGE.__contains__('timeframe') else '1m'
        timesince = KP_GLOBAL_DATERANGE['fromdate'] if KP_GLOBAL_DATERANGE.__contains__('fromdate') else '2022-09-22 00:00:00'
        timesince = 1000 * datetime.strptime(timesince,'%Y-%m-%d %H:%M:%S').timestamp()
        timeend = KP_GLOBAL_DATERANGE['todate'] if KP_GLOBAL_DATERANGE.__contains__('todate') else '2022-09-23 01:45:00'
        timeend = 1000 * datetime.strptime(timeend,'%Y-%m-%d %H:%M:%S').timestamp()
        
        pagelimit = KP_GLOBAL_DATERANGE['limit'] if KP_GLOBAL_DATERANGE.__contains__('limit') else 100
        
        while while_condition:
            retlist = []
            for symbol in KP_GLOBAL_SYMBOLS:
                # print(symbol)
                cc = self.fetch_candles(symbol['symbol'],since=int(timesince), frame=timeframe , limit=pagelimit)
                retlist.append(cc)
                sleep(0.12) #限制 20次/2s
                
            #TODO basis compositing
            print(len(retlist[0]), len(retlist[1]))
            while_condition = False#END while
        #END while
    #END pull
    
    def fetch_candles(self, symbol:str, since:int, frame='1m', limit=100):
        retry_curr = 0
        retry_max = KP_EXCHANGE_CCXT['retry_max'] if KP_EXCHANGE_CCXT.__contains__('retry_max') else 3
        while retry_curr < retry_max:
            try:
                data = self.kp_exchange.fetch_ohlcv(symbol, since=since, timeframe=frame, limit=limit)
                # print(symbol, since, frame, limit)
                return data

            except ccxt.RequestTimeout as e:
                if retry_curr==retry_max-1:
                    logger.error("request timeout, check your proxy or hosts config")
                # traceback.print_exc() #该处可报出异常的具体位置和原因
                # traceback.format_exc() #将异常存入变量a中
                retry_curr += 1
            except ccxt.RateLimitExceeded as e:
                logger.warning("rate limit exceed, sleep 1s")
                sleep(1)
                
        return False
    #END fetch

    def check_exchange_time(self,):
        ##时间对比
        ftime = self.kp_exchange.fetchTime()
        now = datetime.now().timestamp()
        cmptime = ftime-int(now*1000)
        # fdate = datetime.utcfromtimestamp(ftime/1000)
        # ndate = datetime.utcfromtimestamp(now)
        # print(fdate,ndate, cmptime/1000)
        if cmptime > 2000:
            raise RuntimeError(f"exchange time - localtime: {cmptime}ms")
        logger.info(f"Exchange time diff: {cmptime}ms")
        return True
    #END check time

    def check_database_health(self,):
        if KP_GLOBAL_DATABASE['type'] != 'questdb':
            return None
        #check alive
        host = KP_GLOBAL_DATABASE['host']
        port = KP_GLOBAL_DATABASE['health_port']
        
        health_url = f"http://{host}:{port}/status"
        f = request.urlopen(health_url)
        if f.read().decode().index('Healthy') > 0:
            logger.info("QuestDB Status: Healthy")
            return True
        else:
            return False
    #END check health


#END class

def main():
    obj = kp_history()
    obj.run()

if __name__ == '__main__':
    main()









