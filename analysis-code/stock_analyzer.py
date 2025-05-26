import sys
import json
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

# Ensure data_api is available
# This path might need adjustment based on the execution environment of the script.
# Assuming the script is run from the repository root or `analysis-code/`
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Add repo root to path
    sys.path.append('/opt/.manus/.sandbox-runtime') # Standard path for data_api
    from data_api import ApiClient
except ImportError:
    print("Error: Could not import ApiClient. Ensure data_api.py is accessible.")
    # Fallback for local development if data_api.py is in the root directory
    try:
        from data_api import ApiClient
        print("Warning: Imported ApiClient from current directory or Python path, not sandbox path.")
    except ImportError:
        print("Error: ApiClient could not be imported. Please check installation and path.")
        sys.exit(1)


def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Stock Analysis Script")
    parser.add_argument("--ticker", required=True, help="Stock ticker symbol (e.g., AAPL, PLTR)")
    args = parser.parse_args()
    return args.ticker

def main():
    """Main function to run the stock analysis."""
    ticker = parse_arguments()
    print(f"Analyzing stock: {ticker}")

    # Output directory: public/analysis_outputs/
    # Script is in analysis-code/, so use os.path.join to go up one level, then to public/analysis_outputs
    output_dir = os.path.join(os.path.dirname(__file__), "..", "public", "analysis_outputs")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"Created directory: {output_dir}")
    else:
        if not os.path.isdir(output_dir):
            print(f"Error: Output path {output_dir} exists but is not a directory. Exiting.")
            sys.exit(1)

    # --- Step 1: Initialize API Client and Fetch Data ---
    try:
        api_client = ApiClient()
    except Exception as e:
        print(f"Error initializing ApiClient: {e}")
        sys.exit(1)

    stock_data_json = None
    stock_insights_json = None
    stock_holders_json = None

    # Fetch Stock Chart Data
    try:
        print(f"Fetching stock chart data for {ticker} (1d interval, 1y range)...")
        # The API returns data for max 1 year with 1d interval.
        stock_data_json = api_client.get_stock_chart(ticker=ticker, interval="1d", range="1y")
        stock_data_path = os.path.join(output_dir, f"{ticker}_stock_data_raw.json") # Save raw for inspection
        with open(stock_data_path, "w") as f:
            json.dump(stock_data_json, f)
        print(f"Raw stock chart data saved to {stock_data_path}")
        if not stock_data_json or "chart" not in stock_data_json or not stock_data_json["chart"]["result"]:
            print(f"Error: Stock chart data for {ticker} is missing or invalid.")
            sys.exit(1)
    except Exception as e:
        print(f"Error fetching stock chart data for {ticker}: {e}")
        sys.exit(1) # Critical data

    # Fetch Stock Insights Data
    try:
        print(f"Fetching stock insights data for {ticker}...")
        stock_insights_json = api_client.get_stock_insights(ticker=ticker)
        stock_insights_path = os.path.join(output_dir, f"{ticker}_stock_insights_raw.json")
        with open(stock_insights_path, "w") as f:
            json.dump(stock_insights_json, f)
        print(f"Raw stock insights data saved to {stock_insights_path}")
        if not stock_insights_json or "finance" not in stock_insights_json or not stock_insights_json["finance"]["result"]:
             print(f"Warning: Stock insights data for {ticker} is missing or invalid. Some analysis parts might be affected.")
             # Not exiting, as some analysis can proceed without it
    except Exception as e:
        print(f"Error fetching stock insights data for {ticker}: {e}")
        # Depending on how critical this is, you might choose to exit or continue
        # For now, let's allow continuing with a warning, as some analysis might still be possible.
        stock_insights_json = {} # Ensure it's an empty dict to avoid None errors later

    # Fetch Stock Holders Data
    try:
        print(f"Fetching stock holders data for {ticker}...")
        stock_holders_json = api_client.get_stock_holders(ticker=ticker)
        stock_holders_path = os.path.join(output_dir, f"{ticker}_stock_holders_raw.json")
        with open(stock_holders_path, "w") as f:
            json.dump(stock_holders_json, f)
        print(f"Raw stock holders data saved to {stock_holders_path}")
        if not stock_holders_json or "finance" not in stock_holders_json or not stock_holders_json["finance"]["result"]:
            print(f"Warning: Stock holders data for {ticker} is missing or invalid. Some analysis parts might be affected.")
        # Not exiting, allow continuation
    except Exception as e:
        print(f"Error fetching stock holders data for {ticker}: {e}")
        stock_holders_json = {} # Ensure it's an empty dict

    # --- Step 2: Perform Data Processing and Analysis ---
    print("Performing data analysis...")
    
    # Initialize analysis_result with default/empty values
    analysis_result = {
        "basic_info": {},
        "current_price": {},
        "technical_analysis": {},
        "volume_analysis": {},
        "investment_recommendation": {},
        "key_developments": [],
        "insider_trading": [],
        "conclusion": {}
    }

    # Process Stock Chart Data (Primary source for price, volume, MAs)
    meta = {}
    df = pd.DataFrame()

    if stock_data_json and stock_data_json.get("chart", {}).get("result"):
        chart_result = stock_data_json["chart"]["result"][0]
        meta = chart_result.get("meta", {})
        
        timestamps = chart_result.get("timestamp", [])
        ohlcv = chart_result.get("indicators", {}).get("quote", [{}])[0]

        if timestamps and ohlcv:
            df = pd.DataFrame({
                "timestamp": pd.to_datetime(timestamps, unit="s"),
                "open": ohlcv.get("open"),
                "high": ohlcv.get("high"),
                "low": ohlcv.get("low"),
                "close": ohlcv.get("close"),
                "volume": ohlcv.get("volume")
            })
            df.set_index("timestamp", inplace=True)
            df.dropna(subset=["close", "volume"], inplace=True) # Ensure essential data is present
        else:
            print("Error: Timestamps or OHLCV data is missing in stock_data_json. Cannot proceed with price/MA analysis.")
            # If df is empty, subsequent operations will fail or produce empty results.
            # This should be handled gracefully by checks like `if not df.empty:`.
    else:
        print("Error: Critical stock chart data is missing. Analysis will be incomplete.")
        # sys.exit(1) # Or handle as appropriate

    # Basic Info
    analysis_result["basic_info"] = {
        "company_name": meta.get("longName", meta.get("shortName", ticker)), # Fallback to ticker if longName not present
        "symbol": meta.get("symbol", ticker),
        "exchange": meta.get("fullExchangeName", meta.get("exchangeName", "N/A")),
        "currency": meta.get("currency", "N/A")
    }

    # Current Price
    if not df.empty:
        latest_data = df.iloc[-1]
        previous_data = df.iloc[-2] if len(df) >= 2 else latest_data # Handle case with only one data point

        price_change = latest_data["close"] - previous_data["close"]
        price_change_pct = (price_change / previous_data["close"]) * 100 if previous_data["close"] else 0

        analysis_result["current_price"] = {
            "price": meta.get("regularMarketPrice", latest_data["close"]), # Prefer meta, fallback to latest close
            "week52_high": meta.get("fiftyTwoWeekHigh", df["high"].rolling(window=252, min_periods=1).max().iloc[-1] if not df.empty else None),
            "week52_low": meta.get("fiftyTwoWeekLow", df["low"].rolling(window=252, min_periods=1).min().iloc[-1] if not df.empty else None),
            "day_high": meta.get("regularMarketDayHigh", latest_data["high"]),
            "day_low": meta.get("regularMarketDayLow", latest_data["low"]),
            "volume": int(meta.get("regularMarketVolume", latest_data["volume"])), # Ensure volume is int
            "prev_close": meta.get("regularMarketPreviousClose", previous_data["close"]),
            "price_change": price_change,
            "price_change_pct": price_change_pct
        }
    else: # df is empty, try to populate from meta if available, else N/A
        analysis_result["current_price"] = {
            "price": meta.get("regularMarketPrice"),
            "week52_high": meta.get("fiftyTwoWeekHigh"),
            "week52_low": meta.get("fiftyTwoWeekLow"),
            "day_high": meta.get("regularMarketDayHigh"),
            "day_low": meta.get("regularMarketDayLow"),
            "volume": int(meta.get("regularMarketVolume", 0)),
            "prev_close": meta.get("regularMarketPreviousClose"),
            "price_change": None, # Cannot calculate without historical data
            "price_change_pct": None
        }


    # Technical Analysis
    if not df.empty:
        df["MA20"] = df["close"].rolling(window=20, min_periods=1).mean()
        df["MA50"] = df["close"].rolling(window=50, min_periods=1).mean()
        df["MA200"] = df["close"].rolling(window=200, min_periods=1).mean()
        
        latest_ma20 = df["MA20"].iloc[-1]
        latest_ma50 = df["MA50"].iloc[-1]
        latest_ma200 = df["MA200"].iloc[-1]
        latest_close = df["close"].iloc[-1]

        # MA Cross Status
        ma_cross_status = "데이터 부족"
        if len(df) >= 50: # Need enough data for MA50
            # Check MA20 vs MA50 for golden/dead cross
            # Golden Cross: MA20 crosses above MA50
            # Dead Cross: MA20 crosses below MA50
            prev_ma20_gt_ma50 = df["MA20"].iloc[-2] > df["MA50"].iloc[-2] if len(df) >= 2 else False
            curr_ma20_gt_ma50 = latest_ma20 > latest_ma50

            if curr_ma20_gt_ma50 and not prev_ma20_gt_ma50:
                ma_cross_status = f"최근 20일/50일 이동평균선 골든크로스 발생 (단기 상승 신호)"
            elif not curr_ma20_gt_ma50 and prev_ma20_gt_ma50:
                ma_cross_status = f"최근 20일/50일 이동평균선 데드크로스 발생 (단기 하락 신호)"
            elif curr_ma20_gt_ma50:
                ma_cross_status = f"20일 이동평균선이 50일 이동평균선 위에 위치 (단기 상승세 유지)"
            else:
                ma_cross_status = f"20일 이동평균선이 50일 이동평균선 아래에 위치 (단기 하락세 유지)"
        
        ma_long_cross_status = "데이터 부족"
        if len(df) >= 200: # Need enough data for MA200
            # Check MA50 vs MA200 for golden/dead cross
            prev_ma50_gt_ma200 = df["MA50"].iloc[-2] > df["MA200"].iloc[-2] if len(df) >= 2 else False # Requires at least 2 data points for comparison
            curr_ma50_gt_ma200 = latest_ma50 > latest_ma200

            if curr_ma50_gt_ma200 and not prev_ma50_gt_ma200:
                ma_long_cross_status = f"최근 50일/200일 이동평균선 골든크로스 발생 (장기 상승 신호)"
            elif not curr_ma50_gt_ma200 and prev_ma50_gt_ma200:
                ma_long_cross_status = f"최근 50일/200일 이동평균선 데드크로스 발생 (장기 하락 신호)"
            elif curr_ma50_gt_ma200:
                ma_long_cross_status = f"50일 이동평균선이 200일 이동평균선 위에 위치 (장기 상승세 유지)"
            else:
                ma_long_cross_status = f"50일 이동평균선이 200일 이동평균선 아래에 위치 (장기 하락세 유지)"

        # Trend (simplified based on MA positions)
        trend = "중립"
        if latest_close > latest_ma20 and latest_ma20 > latest_ma50 and latest_ma50 > latest_ma200:
            trend = "강한 상승"
        elif latest_close > latest_ma20 and latest_ma20 > latest_ma50:
            trend = "상승"
        elif latest_close < latest_ma20 and latest_ma20 < latest_ma50 and latest_ma50 < latest_ma200:
            trend = "강한 하락"
        elif latest_close < latest_ma20 and latest_ma20 < latest_ma50:
            trend = "하락"
        elif latest_ma20 > latest_ma50 and latest_ma50 > latest_ma200: # Price might be lagging but MAs are aligned
             trend = "상승 추세"
        elif latest_ma20 < latest_ma50 and latest_ma50 < latest_ma200:
             trend = "하락 추세"


        analysis_result["technical_analysis"] = {
            "ma_20": latest_ma20,
            "ma_50": latest_ma50,
            "ma_200": latest_ma200,
            "ma_cross_status": ma_cross_status,
            "ma_long_cross_status": ma_long_cross_status,
            "trend": trend,
            "support_level": None, # To be filled from insights
            "resistance_level": None, # To be filled from insights
            "stop_loss": None # To be filled from insights (or calculated if logic provided)
        }
    else: # df is empty
         analysis_result["technical_analysis"] = {
            "ma_20": None, "ma_50": None, "ma_200": None,
            "ma_cross_status": "데이터 부족", "ma_long_cross_status": "데이터 부족",
            "trend": "데이터 부족",
            "support_level": None, "resistance_level": None, "stop_loss": None
        }


    # Volume Analysis
    if not df.empty and 'volume' in df.columns:
        df["VolumeMA20"] = df["volume"].rolling(window=20, min_periods=1).mean()
        latest_volume = df["volume"].iloc[-1]
        latest_volume_ma20 = df["VolumeMA20"].iloc[-1]
        
        volume_change_pct = ((latest_volume / latest_volume_ma20) - 1) * 100 if latest_volume_ma20 else 0
        
        volume_text = "거래량 정보 부족"
        if latest_volume_ma20 > 0: # Avoid division by zero if MA is zero
            if latest_volume > latest_volume_ma20 * 1.5: # More than 50% above MA
                volume_text = f"최근 거래량({int(latest_volume):,})이 20일 평균({int(latest_volume_ma20):,}) 대비 {volume_change_pct:.2f}% 증가하며 매우 활발합니다."
            elif latest_volume > latest_volume_ma20 * 1.1: # More than 10% above MA
                volume_text = f"최근 거래량({int(latest_volume):,})이 20일 평균({int(latest_volume_ma20):,}) 대비 {volume_change_pct:.2f}% 증가하며 활발한 편입니다."
            elif latest_volume < latest_volume_ma20 * 0.7: # Less than 70% of MA
                volume_text = f"최근 거래량({int(latest_volume):,})이 20일 평균({int(latest_volume_ma20):,}) 대비 {volume_change_pct:.2f}% 감소하며 상대적으로 저조합니다."
            else:
                volume_text = f"최근 거래량({int(latest_volume):,})은 20일 평균({int(latest_volume_ma20):,}) 수준을 유지하고 있습니다 ({volume_change_pct:.2f}%)."

        analysis_result["volume_analysis"] = {
            "volume_latest": int(latest_volume),
            "volume_ma_20": int(latest_volume_ma20),
            "volume_change_pct": volume_change_pct,
            "volume_analysis": volume_text
        }
    else: # df is empty or no volume
        analysis_result["volume_analysis"] = {
            "volume_latest": analysis_result["current_price"].get("volume"), # Try to get from current_price if available
            "volume_ma_20": None,
            "volume_change_pct": None,
            "volume_analysis": "거래량 데이터 부족"
        }


    # Process Stock Insights Data
    insights_data = {}
    key_technicals = {}
    recommendation_trend = []
    company_snapshot = {}
    if stock_insights_json and stock_insights_json.get("finance", {}).get("result"):
        insights_data = stock_insights_json["finance"]["result"]
        key_technicals = insights_data.get("instrumentInfo", {}).get("keyTechnicals", {})
        recommendation_trend_data = insights_data.get("recommendationTrend", {}).get("trend", [])
        # Ensure recommendation_trend is a list of dicts, not a single dict
        if isinstance(recommendation_trend_data, list):
            recommendation_trend = recommendation_trend_data
        elif isinstance(recommendation_trend_data, dict): # Sometimes it might be a single dict
             recommendation_trend = [recommendation_trend_data]


        company_snapshot = insights_data.get("companySnapshot", {})
        # Extract key developments
        # Assuming 'news' or 'events' might be part of companySnapshot or a dedicated section
        # For now, using a placeholder if specific path isn't clear from pltr_analysis_code.md
        # The example showed "key_developments": insights_result.get("finance", {}).get("result", {}).get("companySnapshot", {}).get("company", {}).get("hiring", [])
        # This seems like an example, let's look for something more generic like 'news'
        # For PLTR example, "key_developments" was empty. Let's try to find a common path.
        # Yahoo Finance API often has 'secFilings' or 'news'. 'companyEvents' might be under 'esgScores'.
        # Let's use a placeholder structure for now and assume insights data might have a 'companyEvents' or similar.
        # Based on typical Yahoo Finance structures, 'news' is often found under quoteSummary.
        # Since `get_stock_insights` structure is not fully detailed, we'll make a best guess.
        # Let's assume insights_data.get("news") or similar.
        # The example used 'company.hiring' which is very specific.
        # A more robust approach might be to look for a news/events list.
        # If `pltr_analysis_code.md`'s "key_developments" was derived from a specific part of the API response,
        # that path should be used. The previous script used `insights_result.get("finance", {}).get("result", {}).get("companySnapshot", {}).get("company", {}).get("hiring", [])`
        # Let's stick to that for now if that's what the example implied.
        hiring_info = insights_data.get("companySnapshot", {}).get("company", {}).get("hiring", [])
        if hiring_info and isinstance(hiring_info, list): # Ensure it's a list
             for item in hiring_info: # This path seems too specific for general "key developments"
                 # Let's try to find a more generic news source if available, else use this.
                 # For now, the `pltr_analysis_code.md` implies this path, so we'll use it.
                 # A real "key development" would have a date and headline. Hiring info might not.
                 # Re-evaluating: `pltr_analysis_code.md` had `key_developments: []`
                 # Let's assume we need to find a proper news source.
                 # `getSummary` endpoint often has news. `get_stock_insights` might be different.
                 # Let's assume `insights_data.get("news")` or `insights_data.get("companyNews")`
                 # For now, if not found, it will be an empty list.
                 pass # Placeholder, will refine if a specific path for news is identified
        
        # Based on the PLTR example, "key_developments" was an empty list.
        # If the API provided a news section (e.g., `insights_data.get('news', [])`), it would be processed here.
        # Example:
        # raw_news = insights_data.get('news', [])
        # for news_item in raw_news:
        # analysis_result["key_developments"].append({
        # "date": news_item.get("providerPublishTime") # Needs conversion to date string
        # "headline": news_item.get("title")
        # })
        # For now, it remains empty as per PLTR example unless data is found.


    # Populate from key_technicals if available
    if key_technicals:
        analysis_result["technical_analysis"]["support_level"] = key_technicals.get("support")
        analysis_result["technical_analysis"]["resistance_level"] = key_technicals.get("resistance")
        analysis_result["technical_analysis"]["stop_loss"] = key_technicals.get("stopLossPrice") # Or "stopLoss"
    
    # Investment Recommendation
    # The PLTR example had target_price, provider, rating.
    # This usually comes from recommendationTrend or financialData.
    target_price = insights_data.get("financialData", {}).get("targetMeanPrice", {}).get("raw")
    provider = "Multiple Analysts" # Default if specific provider isn't in recommendationTrend
    rating = "N/A" # Default
    
    if recommendation_trend: # This is a list of dicts
        # Use the latest recommendation (assuming sorted or take the first one)
        latest_rec = recommendation_trend[0] if recommendation_trend else {}
        rating_map = {"BUY": "매수", "STRONG_BUY": "적극 매수", "HOLD": "중립", "SELL": "매도", "STRONG_SELL": "적극 매도", "UNDERPERFORM": "시장수익률 하회", "OVERWEIGHT": "비중 확대"}
        raw_rating = latest_rec.get("strongBuy", 0) > 0 and "STRONG_BUY" or \
                     latest_rec.get("buy", 0) > 0 and "BUY" or \
                     latest_rec.get("hold", 0) > 0 and "HOLD" or \
                     latest_rec.get("sell", 0) > 0 and "SELL" or \
                     latest_rec.get("strongSell", 0) > 0 and "STRONG_SELL" or "N/A"
        
        # The `recommendationTrend` array usually has `period`, `strongBuy`, `buy`, `hold`, `sell`, `strongSell` counts.
        # We need to derive a single 'rating' like "BUY".
        # A common way is to see which rating has the highest count for the most recent period.
        # Or, some APIs provide `recommendations.rating`.
        # The `pltr_analysis_code.md` implies a single "rating" field.
        # Let's try to get `financialData.recommendationKey`
        api_rating = insights_data.get("financialData", {}).get("recommendationKey")
        if api_rating and api_rating.upper() in rating_map:
            rating = rating_map[api_rating.upper()]
        elif raw_rating != "N/A": # Fallback to derived from counts
             rating = rating_map.get(raw_rating, "N/A")


        # Provider might be more general if derived from recommendationTrend.
        # If `insights_data.get("quoteSummary", {}).get("recommendationTrend", {}).get("trend")` has provider info, use it.
        # For now, "Multiple Analysts" is a safe bet.
    
    investment_opinion = f"{analysis_result['basic_info']['company_name']}에 대한 투자 의견은 현재 '{rating}'입니다."
    if target_price:
        investment_opinion += f" 분석가들은 평균적으로 {target_price:.2f} {analysis_result['basic_info']['currency']}의 목표 주가를 제시하고 있습니다."
    else:
        investment_opinion += " 현재 구체적인 목표 주가 정보는 제공되지 않았습니다."

    if rating in ["매수", "적극 매수"]:
        investment_opinion += " 이는 현재 주가 수준에서 상승 잠재력이 있다고 판단될 수 있습니다."
    elif rating in ["매도", "적극 매도"]:
        investment_opinion += " 이는 현재 주가 수준에서 하락 위험이 있거나 고평가 되었다고 판단될 수 있습니다."
    else: # 중립
        investment_opinion += " 이는 현재 주가가 적정 수준이거나, 뚜렷한 상승/하락 요인이 부족하다고 판단될 수 있습니다."


    analysis_result["investment_recommendation"] = {
        "target_price": target_price,
        "provider": provider, # This might need to be extracted if available, else 'Multiple Analysts'
        "rating": rating,
        "investment_opinion": investment_opinion
    }

    # Process Stock Holders Data
    if stock_holders_json and stock_holders_json.get("finance", {}).get("result"):
        holders_result = stock_holders_json["finance"]["result"]
        # Insider Trading (Example structure, may need adjustment based on actual API response)
        # The PLTR example had: [{'name': ..., 'relation': ..., 'transaction': ..., 'date': ..., 'position': ...}]
        # This usually comes from `insiderTransactions.transactions`
        insider_transactions_raw = holders_result.get("insiderTransactions", {}).get("transactions", [])
        if isinstance(insider_transactions_raw, list): # Ensure it's a list
            for trans in insider_transactions_raw:
                if not isinstance(trans, dict): continue # Skip if not a dict
                # Date conversion: 'startDate.fmt' is usually 'YYYY-MM-DD'
                transaction_date = trans.get("startDate", {}).get("fmt", "N/A")
                # Transaction text: 'transactionText' or build from 'shares' and 'value'
                transaction_text = trans.get("transactionText", "")
                if not transaction_text and trans.get("shares", {}).get("raw") and trans.get("value", {}).get("raw"):
                    action = "매수" if trans.get("value", {}).get("raw") > 0 else "매도" # Assuming positive value is buy
                    transaction_text = f"{abs(trans['shares']['raw']):,}주 {action} (약 {abs(trans['value']['raw']):,} {analysis_result['basic_info']['currency']})"
                elif not transaction_text and trans.get("ownership", {}).get("raw") in [1,4]: # 1 for Direct, 4 for Indirect. Check API docs.
                    # This might be a holding report, not a transaction.
                    transaction_text = f"보유 변동: {trans.get('shares', {}).get('longFmt', 'N/A')}"


                analysis_result["insider_trading"].append({
                    "name": trans.get("filerName", "N/A"),
                    "relation": trans.get("filerRelation", "N/A"),
                    "transaction": transaction_text,
                    "date": transaction_date,
                    "position": trans.get("filerTitle", "N/A") # 'filerTitle' or 'position'
                })
        else:
            print(f"Warning: Insider transactions data for {ticker} is not in the expected list format.")


    # Conclusion - This should synthesize information
    conc_trend = analysis_result["technical_analysis"].get("trend", "데이터 부족")
    conc_trend_analysis = f"{analysis_result['basic_info']['company_name']}의 현재 주가 추세는 '{conc_trend}'으로 평가됩니다. "
    if conc_trend == "강한 상승":
        conc_trend_analysis += "모든 주요 이동평균선(20일, 50일, 200일)이 정배열을 이루고 주가가 그 위에 있어 매우 긍정적인 신호입니다."
    elif conc_trend == "상승":
        conc_trend_analysis += "단기 및 중기 이동평균선(20일, 50일)이 상승세를 보이고 있으며, 주가가 이들 선 위에 위치해 긍정적입니다."
    elif conc_trend == "하락":
        conc_trend_analysis += "단기 및 중기 이동평균선(20일, 50일)이 하락세를 보이고 있으며, 주가가 이들 선 아래에 위치해 주의가 필요합니다."
    elif conc_trend == "강한 하락":
        conc_trend_analysis += "모든 주요 이동평균선(20일, 50일, 200일)이 역배열을 이루고 주가가 그 아래에 있어 부정적인 신호가 강합니다."
    else: # 중립 or 데이터 부족
        conc_trend_analysis += "주가가 이동평균선들 사이에서 혼조세를 보이거나, 뚜렷한 방향성을 찾기 어렵습니다. 추가적인 분석이 필요합니다."
    
    # Add MA cross status to trend analysis
    ma_cross_status_text = analysis_result["technical_analysis"].get("ma_cross_status", "")
    if "골든크로스" in ma_cross_status_text:
        conc_trend_analysis += f" 특히, {ma_cross_status_text}는 단기적으로 긍정적인 모멘텀을 시사합니다."
    elif "데드크로스" in ma_cross_status_text:
        conc_trend_analysis += f" 특히, {ma_cross_status_text}는 단기적으로 부정적인 모멘텀을 시사합니다."

    ma_long_cross_status_text = analysis_result["technical_analysis"].get("ma_long_cross_status", "")
    if "골든크로스" in ma_long_cross_status_text:
        conc_trend_analysis += f" 또한, {ma_long_cross_status_text}는 장기적으로도 긍정적인 전망을 강화합니다."
    elif "데드크로스" in ma_long_cross_status_text:
        conc_trend_analysis += f" 또한, {ma_long_cross_status_text}는 장기적으로도 주의가 필요함을 나타냅니다."


    analysis_result["conclusion"] = {
        "trend": conc_trend,
        "trend_analysis": conc_trend_analysis,
        "volume_analysis": analysis_result["volume_analysis"].get("volume_analysis", "거래량 분석 데이터 부족"),
        "investment_opinion": analysis_result["investment_recommendation"].get("investment_opinion", "투자 의견 정보 부족")
    }

    # Save Analysis Result JSON
    analysis_result_path = os.path.join(output_dir, f"{ticker}_analysis_result.json")
    try:
        with open(analysis_result_path, "w", encoding="utf-8") as f: # Ensure utf-8 for Korean characters
            json.dump(analysis_result, f, indent=4, ensure_ascii=False)
        print(f"Analysis results saved to {analysis_result_path}")
    except Exception as e:
        print(f"Error saving analysis JSON: {e}")


    # --- Step 3: Generate Charts ---
    if not df.empty:
        try:
            print("Generating charts...")
            plt.style.use('seaborn-v0_8-darkgrid')
            fig, axes = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})
            
            # Price Chart with MA20, MA50, MA200
            axes[0].plot(df.index, df["close"], label=f"{ticker} 종가", color="blue", alpha=0.7)
            if "MA20" in df.columns: axes[0].plot(df.index, df["MA20"], label="MA20", color="orange", linestyle="--", alpha=0.9)
            if "MA50" in df.columns: axes[0].plot(df.index, df["MA50"], label="MA50", color="green", linestyle="--", alpha=0.9)
            if "MA200" in df.columns: axes[0].plot(df.index, df["MA200"], label="MA200", color="red", linestyle="--", alpha=0.9)
            
            axes[0].set_title(f"{analysis_result['basic_info']['company_name']} ({ticker}) 주가 및 이동평균선", fontsize=16)
            axes[0].set_ylabel(f"주가 ({analysis_result['basic_info']['currency']})", fontsize=12)
            axes[0].legend(fontsize=10)
            axes[0].grid(True, which='both', linestyle='--', linewidth=0.5)
            
            # Volume Chart
            if "volume" in df.columns and "VolumeMA20" in df.columns:
                axes[1].bar(df.index, df["volume"], label="거래량", color="grey", alpha=0.5)
                axes[1].plot(df.index, df["VolumeMA20"], label="거래량 MA20", color="purple", linestyle="--", alpha=0.9)
                axes[1].set_title(f"{ticker} 거래량", fontsize=14)
                axes[1].set_ylabel("거래량", fontsize=12)
                axes[1].legend(fontsize=10)
                axes[1].grid(True, which='both', linestyle='--', linewidth=0.5)
            
            axes[1].set_xlabel("날짜", fontsize=12)
            plt.tight_layout()
            chart_path = os.path.join(output_dir, f"{ticker}_stock_chart.png")
            plt.savefig(chart_path)
            plt.close() 
            print(f"Stock chart saved to {chart_path}")

        except Exception as e:
            print(f"Error generating charts: {e}")
    else:
        print("Skipping chart generation as no stock data is available (df is empty).")


    # --- Step 4: Calculate and Save Technical Indicators CSV ---
    if not df.empty:
        try:
            print("Calculating technical indicators for CSV...")
            df_tech = pd.DataFrame(index=df.index) # Use original df index
            df_tech["close"] = df["close"] # Ensure 'close' is present for calculations

            # RSI
            delta = df_tech["close"].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14, min_periods=1).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14, min_periods=1).mean()
            rs = gain / loss
            df_tech["RSI"] = 100 - (100 / (1 + rs))
            df_tech["RSI"].fillna(50, inplace=True) # Fill initial NaNs with 50 (neutral)

            # Bollinger Bands
            df_tech["MA20_BB"] = df_tech["close"].rolling(window=20, min_periods=1).mean()
            df_tech["STD20_BB"] = df_tech["close"].rolling(window=20, min_periods=1).std().fillna(0) # Fill NaN std with 0
            df_tech["Upper_BB"] = df_tech["MA20_BB"] + (df_tech["STD20_BB"] * 2)
            df_tech["Lower_BB"] = df_tech["MA20_BB"] - (df_tech["STD20_BB"] * 2)

            # MACD
            df_tech["EMA12"] = df_tech["close"].ewm(span=12, adjust=False, min_periods=1).mean()
            df_tech["EMA26"] = df_tech["close"].ewm(span=26, adjust=False, min_periods=1).mean()
            df_tech["MACD"] = df_tech["EMA12"] - df_tech["EMA26"]
            df_tech["Signal_Line"] = df_tech["MACD"].ewm(span=9, adjust=False, min_periods=1).mean()

            # Select relevant columns and last 1 year of data (approx 252 trading days)
            # Or, as per pltr_analysis_code.md, it saved for the whole period.
            # The original script saved tail(30). Let's save the whole period available from df.
            technical_indicators_df = df_tech[["RSI", "Upper_BB", "Lower_BB", "MACD", "Signal_Line", "MA20_BB", "close"]]
            
            technical_indicators_path = os.path.join(output_dir, f"{ticker}_technical_indicators.csv")
            technical_indicators_df.to_csv(technical_indicators_path)
            print(f"Technical indicators saved to {technical_indicators_path}")

        except Exception as e:
            print(f"Error calculating or saving technical indicators: {e}")
    else:
        print("Skipping technical indicators CSV generation as no stock data is available (df is empty).")


    print(f"Stock analysis script for {ticker} completed.")

if __name__ == "__main__":
    # Set Matplotlib backend to Agg to avoid GUI issues in headless environments
    try:
        import matplotlib
        matplotlib.use('Agg')
        # Set Korean font
        # plt.rcParams['font.family'] = 'NanumGothic' # Example, ensure font is installed
        # Fallback to a generic sans-serif if NanumGothic is not available
        try:
            plt.rcParams['font.family'] = 'NanumGothic'
            # Test if font is available
            _ = plt.figure() 
            plt.title("테스트")
            plt.close(_)
        except:
            print("Warning: NanumGothic font not found. Using default sans-serif. Korean text in charts might not display correctly.")
            plt.rcParams['font.family'] = 'sans-serif'

    except ImportError:
        print("Warning: Matplotlib not found. Charts will not be generated.")
    except Exception as e:
        print(f"Error setting Matplotlib backend or font: {e}")
    
    main()
