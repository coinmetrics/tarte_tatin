import os

from coinmetrics.api_client import CoinMetricsClient

api_key = os.getenv("CM_API_KEY")
client = CoinMetricsClient(api_key)

example = client.get_market_candles(
    markets='upbit-aave-krw-spot',
    start_time='2025-03-19',
    frequency='1h'
).to_dataframe()

print(example.iloc[0])
