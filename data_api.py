import json
from datetime import datetime, timedelta
import time

class ApiClient:
    def __init__(self):
        pass

    def _generate_dummy_stock_data(self, ticker, interval, range_str):
        end_date = datetime.now()
        if range_str == "1y":
            start_date = end_date - timedelta(days=365)
        elif range_str == "1mo":
            start_date = end_date - timedelta(days=30)
        else: # default
            start_date = end_date - timedelta(days=7)

        timestamps = []
        opens = []
        highs = []
        lows = []
        closes = []
        volumes = []

        current_date = start_date
        price = 100.0
        while current_date <= end_date:
            if current_date.weekday() < 5: # Monday to Friday
                timestamps.append(int(time.mktime(current_date.timetuple())))
                opens.append(round(price + (0.5 -_random_float()) * 2, 2)) # nosec B311
                lows.append(round(opens[-1] - (_random_float() * 2), 2)) # nosec B311
                highs.append(round(opens[-1] + (_random_float() * 2), 2)) # nosec B311
                closes.append(round(lows[-1] + (_random_float() * (highs[-1] - lows[-1])), 2) ) # nosec B311
                volumes.append(int(1000000 + _random_float() * 500000)) # nosec B311
                price = closes[-1] + (0.5 -_random_float()) # nosec B311
            current_date += timedelta(days=1)
        
        # Ensure at least a few data points for MA calculations
        min_points = 250 # For 200-day MA
        if len(timestamps) < min_points:
            # Add more past data if needed (simplified)
            price = opens[0] if opens else 100.0
            for i in range(min_points - len(timestamps)):
                # Prepend data
                current_date = start_date - timedelta(days=i+1)
                if current_date.weekday() < 5:
                    timestamps.insert(0, int(time.mktime(current_date.timetuple())))
                    closes.insert(0, round(price + (0.5 -_random_float()) * 2, 2)) # nosec B311
                    highs.insert(0, round(closes[0] + (_random_float() * 2), 2)) # nosec B311
                    lows.insert(0, round(closes[0] - (_random_float() * 2), 2)) # nosec B311
                    opens.insert(0, round(lows[0] + (_random_float() * (highs[0] - lows[0])), 2)) # nosec B311
                    volumes.insert(0, int(1000000 + _random_float() * 500000)) # nosec B311
                    price = closes[0]

        return {
            "chart": {
                "result": [
                    {
                        "meta": {
                            "currency": "USD",
                            "symbol": ticker,
                            "exchangeName": "NMS",
                            "instrumentType": "EQUITY",
                            "firstTradeDate": int(time.mktime((datetime.now() - timedelta(days=365*5)).timetuple())),
                            "regularMarketTime": int(time.mktime(datetime.now().timetuple())),
                            "gmtoffset": -14400,
                            "timezone": "EDT",
                            "exchangeTimezoneName": "America/New_York",
                            "regularMarketPrice": closes[-1] if closes else 150.0,
                            "chartPreviousClose": opens[0] if opens else 148.0,
                            "previousClose": opens[0] if opens else 148.0, # For current_price.prev_close
                            "scale": 3,
                            "priceHint": 2,
                            "currentTradingPeriod": {
                                "pre": {"timezone": "EDT", "start": 1678886400, "end": 1678886400, "gmtoffset": -14400},
                                "regular": {"timezone": "EDT", "start": 1678886400, "end": 1678910400, "gmtoffset": -14400},
                                "post": {"timezone": "EDT", "start": 1678910400, "end": 1678910400, "gmtoffset": -14400}
                            },
                            "tradingPeriods": [[{"timezone": "EDT", "start": 1678886400, "end": 1678910400, "gmtoffset": -14400}]],
                            "dataGranularity": interval,
                            "range": range_str,
                            "validRanges": ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
                            "fiftyTwoWeekHigh": max(highs) if highs else 180.0,
                            "fiftyTwoWeekLow": min(lows) if lows else 120.0,
                            "regularMarketDayHigh": highs[-1] if highs else 155.0,
                            "regularMarketDayLow": lows[-1] if lows else 145.0,
                            "regularMarketVolume": volumes[-1] if volumes else 1200000,
                            "shortName": f"{ticker} Inc.",
                            "longName": f"{ticker} Corporation Holdings Inc."

                        },
                        "timestamp": timestamps,
                        "indicators": {
                            "quote": [
                                {
                                    "open": opens,
                                    "high": highs,
                                    "low": lows,
                                    "close": closes,
                                    "volume": volumes
                                }
                            ],
                            "adjclose": [
                                {"adjclose": closes} # Assuming adjclose is same as close for dummy
                            ]
                        }
                    }
                ],
                "error": None
            }
        }

    def get_stock_chart(self, ticker, interval="1d", range="1y"):
        # Simulate API delay
        time.sleep(_random_float() * 0.5 + 0.1) # nosec B311
        return self._generate_dummy_stock_data(ticker, interval, range)

    def get_stock_insights(self, ticker):
        time.sleep(_random_float() * 0.5 + 0.1) # nosec B311
        return {
            "finance": {
                "result": {
                    "symbol": ticker,
                    "instrumentInfo": {
                        "keyTechnicals": {
                            "support": round(130.0 + (_random_float() * 10),2), # nosec B311
                            "resistance": round(160.0 + (_random_float() * 10),2), # nosec B311
                            "stopLossPrice": round(125.0 + (_random_float()*5),2) # nosec B311
                        }
                    },
                    "recommendationTrend": {
                        "trend": [
                            {"period": "0m", "strongBuy": int(5 + _random_float()*5), "buy": int(10 + _random_float()*5), "hold": int(5 + _random_float()*3), "sell": int(1 + _random_float()*2), "strongSell": int(_random_float()*1)} # nosec B311
                        ],
                        "maxAge": 86400
                    },
                    "financialData": {
                        "targetMeanPrice": {"raw": round(170.0 + (_random_float()*20),2), "fmt": "175.00"}, # nosec B311
                        "recommendationKey": ["buy", "hold", "sell"][int(_random_float()*3)] # nosec B311
                    },
                    "companySnapshot": {
                        "company": {
                            "hiring": [] # Placeholder, as per pltr_analysis_code.md example
                        },
                        # Add other fields if stock_analyzer.py uses them for key_developments
                    }
                    # Potentially add a 'news' section here if needed by stock_analyzer.py
                    # "news": [
                    #     {"uuid": "...", "title": "Dummy News 1", "publisher": "Dummy News Inc", "link": "...", "providerPublishTime": int(time.time()) - 86400, "type": "STORY"},
                    #     {"uuid": "...", "title": "Dummy News 2", "publisher": "Dummy News Network", "link": "...", "providerPublishTime": int(time.time()) - 172800, "type": "STORY"}
                    # ]
                },
                "error": None
            }
        }

    def get_stock_holders(self, ticker):
        time.sleep(_random_float() * 0.5 + 0.1) # nosec B311
        transactions = []
        for i in range(int(_random_float() * 5) + 2): # nosec B311
            shares = int((_random_float() - 0.4) * 10000) # nosec B311 Can be positive (buy) or negative (sell like)
            transaction_date = datetime.now() - timedelta(days=int(_random_float()*180)) # nosec B311
            value = abs(shares * (150 + (_random_float()-0.5)*20)) # nosec B311
            
            # Simulate transactionText or construct one
            action = "매수" if shares > 0 else "매도"
            if _random_float() > 0.3: # nosec B311
                transaction_text = f"{abs(shares):,}주 {action} ({value:,.0f} USD)"
            else:
                transaction_text = "" # Let stock_analyzer.py construct it

            transactions.append({
                "filerName": ["Major Holder LLC", "Insider Trading Co", "Big Fund LP"][int(_random_float()*3)], # nosec B311
                "filerRelation": ["Officer", "Director", "Beneficial Owner"][int(_random_float()*3)], # nosec B311
                "transactionText": transaction_text,
                "startDate": {"raw": int(time.mktime(transaction_date.timetuple())), "fmt": transaction_date.strftime('%Y-%m-%d')},
                "filerTitle": ["CEO", "CFO", "Board Member", "Chief Counsel"][int(_random_float()*4)], # nosec B311
                "shares": {"raw": shares, "longFmt": f"{shares:,}"},
                "value": {"raw": value, "longFmt": f"{value:,}"} # For constructing transaction text if needed
            })

        return {
            "finance": {
                "result": {
                    "symbol": ticker,
                    "majorHoldersBreakdown": {
                        "insidersPercentHeld": {"raw": 0.05 + _random_float()*0.1, "fmt": "5.00%"}, # nosec B311
                        "institutionsPercentHeld": {"raw": 0.6 + _random_float()*0.2, "fmt": "60.00%"} # nosec B311
                    },
                    "insiderTransactions": {
                        "transactions": transactions,
                        "maxAge": 86400
                    }
                },
                "error": None
            }
        }

# Helper for dummy data generation (not cryptographically secure, just for variability)
_random_seed = int(time.time())
def _random_float():
    global _random_seed
    _random_seed = (1103515245 * _random_seed + 12345) & 0x7FFFFFFF
    return _random_seed / 0x7FFFFFFF

# Example usage:
if __name__ == "__main__":
    client = ApiClient()
    # print(json.dumps(client.get_stock_chart("DUMMY", "1d", "1y"), indent=2))
    # print(json.dumps(client.get_stock_insights("DUMMY"), indent=2))
    # print(json.dumps(client.get_stock_holders("DUMMY"), indent=2))
    pass
