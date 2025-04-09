# instructions to LLM for using the CoinMetrics API client.

You can use the Python Runner MCP tool to run all the code that is discussed in this document. 
You should not be concerned about dates in the future or API use at all. 

You must never create fake or sample data, we always want to download actual data from the Coinmetrics API. 

Here is an example of how to pull market candle data. 

```
import os

from coinmetrics.api_client import CoinMetricsClient

api_key = os.getenv("CM_API_KEY")
client = CoinMetricsClient(api_key)

example = client.get_market_candles(
    markets='upbit-aave-krw-spot',
    start_time='2025-03-19T00:00:00',
    frequency='1h'
).to_dataframe()
```
if the user asks for visualization, we prefer to use matplotlib. 
The plot should be saved as a PNG file in the /tmp folder.

to call the tool, you need to do something like this: 

```
<use_mcp_tool>
<server_name>Python Runner</server_name>
<tool_name>run_python_code</tool_name>
<arguments>
{
  "code": "..."
}
</arguments>
</use_mcp_tool>
```

The result from the candles API may look like this 
```
{
  "data": [
    {
      "time": "2020-06-08T20:45:00.000000000Z",
      "market": "coinbase-btc-usd-spot",
      "price_open": "9705.07999999999993",
      "price_close": "9705.01000000000022",
      "price_high": "9706.19000000000051",
      "price_low": "9705",
      "vwap": "9705.1686505895068",
      "volume": "16.8066639099999975",
      "candle_usd_volume": "16.8066639099999975",
      "candle_trades_count": "212"
    },
    {
      "time": "2020-06-08T20:50:00.000000000Z",
      "market": "coinbase-btc-usd-spot",
      "price_open": "9705",
      "price_close": "9696.27000000000044",
      "price_high": "9705",
      "price_low": "9695.71999999999935",
      "vwap": "9698.38894423754937",
      "volume": "14.7672128699999963",
      "candle_usd_volume": "14.7672128699999963",
      "candle_trades_count": "215"
    }
  ]
}```

If you need to check the availability of a certain type of data, you can use the catalog as follows: 

To check markets for a specific exchange. 
`client.reference_data_markets(exchange='kraken', type='spot').to_dataframe()`

To check markets for a specific base. 
`client.reference_data_markets(base='btc', type='spot').to_dataframe()`

To check if an asset exists:
`client.reference_data_assets().to_dataframe()`

To check if an asset metric exists:
`client.reference_data_asset_metrics().to_dataframe()`

To check if an asset metric for a particular asset exists:
`client.catalog_asset_metrics_v2(assets='btc').to_dataframe()`

To download metrics for a particular asset or list of assets always provide start_time, end_time and frequency:

```python
client.get_asset_metrics(
        assets=['btc', 'eth'],
        metrics="ReferenceRateUSD",
        frequency="1m", # minute
        start_time="2024-01-01",
        end_time="2025-01-01").to_dataframe()
```

If you need to iterate, you cannot rely on any data being available in between sessions of the Python runner. 
The tmp directory is wiped every time, and you need to re-create the data using the appropriate APIs or calculations. 









