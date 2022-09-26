"""
    拉取历史ohlcv数据
"""
from time import sleep#
from urllib import request#
from datetime import datetime,timezone#

from loguru import logger#
import ccxt#
try:
    import questdb.ingress#
    # from questdb.ingress import Sender, IngressError,TimestampNanos
except ImportError:
    print("use questdb with pip install questdb")

import record as kp_record#

from config import KP_GLOBAL_DATABASE#存储
from config import KP_GLOBAL_DATERANGE#时间区间
from config import KP_GLOBAL_BASIS#基差率
from config import KP_GLOBAL_SYMBOLS#标的
from config import KP_EXCHANGE_CCXT#交易所信息

KP_GLOBAL_TABLE_LABLES = ['ts','open','high','low','close','volume']

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
        
        self.check_exchange_time()
        self.check_database_health()
        
    #END __init__

    def run(self,):
        self.pull_candles()
        

    def pull_candles(self,):
        
        timeframe = KP_GLOBAL_DATERANGE['timeframe'] if KP_GLOBAL_DATERANGE.__contains__('timeframe') else '1m'
        timesince = KP_GLOBAL_DATERANGE['fromdate'] if KP_GLOBAL_DATERANGE.__contains__('fromdate') else '2022-09-22 00:00:00'
        timesince = 1000 * datetime.strptime(timesince,'%Y-%m-%d %H:%M:%S')\
            .replace(tzinfo=timezone.utc).astimezone(tz=timezone.utc).timestamp()
        timeend = KP_GLOBAL_DATERANGE['todate'] if KP_GLOBAL_DATERANGE.__contains__('todate') else '2022-09-23 01:45:00'
        timeend = 1000 * datetime.strptime(timeend,'%Y-%m-%d %H:%M:%S')\
            .replace(tzinfo=timezone.utc).astimezone(tz=timezone.utc).timestamp()
        
        pagelimit = KP_GLOBAL_DATERANGE['limit'] if KP_GLOBAL_DATERANGE.__contains__('limit') else 100
        
        while_condition = True
        time_last = timesince #当time_last >= timeend break
        time_offset = 1000*60*int(timeframe.split('m')[0]) #ms
        
        while while_condition:
            ohlcv_list = []
            cc = [] #ohlcv data onetime
            
            for symbol in KP_GLOBAL_SYMBOLS:
                # print(symbol)
                cc = self.fetch_candles(symbol['symbol'],since=int(timesince), frame=timeframe , limit=pagelimit)
                ohlcv_list.append(cc)
                logger.info(f"get symbol:{symbol['symbol']} data rows:{len(cc)}")
                
                row_last = cc[-1]
                time_last = row_last[0]
                sleep(0.12) #限制 20次/2s
            
            # basis compositing 
            res_list_tuple= self.regrouping_ohlcv_datas(ohlcv_list)
            
            #write to file/db
            self.write_to_db(ohlcv_lsit=res_list_tuple[0], basis_list=res_list_tuple[1])
            
            # print(row_last, time_last)
            logger.info(f"processing ohlcv data from [{self.get_utctime_str(timesince)}] to [{self.get_utctime_str(time_last)}]")
            
            timesince = time_last+time_offset
            while_condition = True if timesince < timeend else False

        #END while
    #END def pull

    @staticmethod
    def get_utctime_str(ts:int) -> str:
        """
        返回格式化的UTC时间

        Args:
            ts (int): 16位时间戳

        Returns:
            str: format string
        """
        return datetime.utcfromtimestamp(ts/1000).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    
    def regrouping_ohlcv_datas(self, ohlcv_list:list, ):
        symbol_num = len(KP_GLOBAL_SYMBOLS)
        i = 0
        res_ohlcv = [] #蜡烛图最终结果
        for ss in KP_GLOBAL_SYMBOLS:
            res_ohlcv.append([])
            
        res_basis = [] #基差率最终结果
        for bb in KP_GLOBAL_BASIS:
            res_basis.append([])
        
        
        while i < len(ohlcv_list[0]):
            
            #处理蜡烛图时间
            j = 0
            while j < symbol_num:
                row = ohlcv_list[j][i]
                row[0] = self.get_utctime_str(row[0])
                res_ohlcv[j].append(row)
                j += 1
            #END symbol
            
            #处理基差率
            j = 0
            while j < len(KP_GLOBAL_BASIS):
                (i_spot,i_future) = KP_GLOBAL_BASIS[j]['combine']
                row_spot = res_ohlcv[i_spot][i]
                row_future = res_ohlcv[i_future][i]

                row = [
                    row_spot[0], #ts
                    round(100*(1+(row_future[1]-row_spot[1])/row_spot[1]), 2),  #open
                    round(100*(1+(row_future[2]-row_spot[2])/row_spot[2]), 2),  #high
                    round(100*(1+(row_future[3]-row_spot[3])/row_spot[3]), 2),  #low
                    round(100*(1+(row_future[4]-row_spot[4])/row_spot[4]), 2),  #close
                    row_future[5], #volume
                ]
                res_basis[j].append(row)
                j += 1
            #END basis
            i += 1
        #END while
        # print( res_basis[0][0])
        return res_ohlcv,res_basis
    #END def regrouping

    def write_to_db(self, ohlcv_lsit, basis_list):
        i=0
        for data in ohlcv_lsit:
            tablename = KP_GLOBAL_SYMBOLS[i]['table']
            self.write_with_record_once(tablename, data)
            i += 1
        
        i=0
        for data in basis_list:
            tablename = KP_GLOBAL_BASIS[i]['table']
            self.write_with_record_once(tablename, data)
            i += 1

    @staticmethod
    def write_with_record_once(tablename, data, dbtype='csv'):
        dbtype = KP_GLOBAL_DATABASE['type'] if KP_GLOBAL_DATABASE.__contains__('type') else dbtype 
        match dbtype:
            case 'csv':
                tablename = f"{KP_GLOBAL_DATABASE['prefix']}{tablename}.csv"
                w_total = kp_record.csv_put_contents(file=tablename, data=data, labels=KP_GLOBAL_TABLE_LABLES)
            case 'questdb':
                pass
            case _:
                raise ValueError(f"no support for database:{dbtype}")
        
        logger.info(f"wirte to {dbtype} in {tablename} total {w_total} rows" )
    #END write 



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
            except ccxt.NetworkError as e:
                logger.warning("network error, sleep 2s")
                sleep(2)
                
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









