CREATE TABLE 'candles_btc-usdt' (
    timestamp TIMESTAMP,
    open float,
    high float,
    low float,
    close float,
    volume float
) TIMESTAMP (timestamp) PARTITION by DAY;


