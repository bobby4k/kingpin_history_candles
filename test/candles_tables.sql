CREATE TABLE 'candles_btc-usdt' (
    timestamp TIMESTAMP,
    open float,
    high float,
    low float,
    close float,
    volume float
) TIMESTAMP (timestamp) PARTITION by DAY;

-- INSERT INTO 'candles_btc-usdt' VALUES(1630425660000000, 48772.2, 48801.4, 48714.6, 48735.5, 1009.0);
SELECT * from 'candles_btc-usdt'

-- INSERT INTO 'candles_btc-usdt' VALUES(1663813260000000, 18527.7, 18527.7, 18518.7, 18519.6, 70.0);
-- TRUNCATE TABLE 'candles_btc-usdt';


-- #表 ETH/USDT
CREATE TABLE 'candles_eth' (
  timestamp TIMESTAMP,
  open FLOAT,
  high FLOAT,
  low FLOAT,
  close FLOAT,
  volume FLOAT
) timestamp (timestamp) PARTITION BY DAY;

-- #表 ETH/USDT:NQ  USDT-221230
CREATE TABLE 'candles_eth-nq' (
  timestamp TIMESTAMP,
  open FLOAT,
  high FLOAT,
  low FLOAT,
  close FLOAT,
  volume FLOAT
) timestamp (timestamp) PARTITION BY DAY;

-- #表 eth当季合约基差率*100
CREATE TABLE 'candles_eth-nq-basis' (
  timestamp TIMESTAMP,
  open FLOAT,
  high FLOAT,
  low FLOAT,
  close FLOAT,
  volume FLOAT
) timestamp (timestamp) PARTITION BY DAY;



