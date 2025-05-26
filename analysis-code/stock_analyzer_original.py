import sys
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np # Though not explicitly used in snippets, good to have for pandas/matplotlib
import argparse
import os

# Ensure data_api is available
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Stock Analysis Script")
    parser.add_argument("--ticker", required=True, help="Stock ticker symbol (e.g., PLTR)")
    args = parser.parse_args()
    return args.ticker

def main():
    """Main function to run the stock analysis."""
    ticker = parse_arguments()
    print(f"Analyzing stock: {ticker}")

    # Create output directory if it doesn't exist
    # The script is in analysis-code/, so ../public/analysis_outputs/ will correctly point to public/analysis_outputs/ at the repo root.
    output_dir = os.path.join("..", "public", "analysis_outputs")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True) # Added exist_ok=True for robustness
        print(f"Created directory: {output_dir}")
    else:
        # Ensure it is a directory if it already exists
        if not os.path.isdir(output_dir):
            print(f"Error: Output path {output_dir} exists but is not a directory. Exiting.")
            sys.exit(1)


    # --- Step 1: Fetch and Save Data ---
    api_client = ApiClient()

    # Fetch Stock Chart Data
    try:
        print(f"Fetching stock chart data for {ticker}...")
        stock_data = api_client.get_stock_chart(ticker=ticker, interval="1d", range="1y")
        stock_data_path = os.path.join(output_dir, f"{ticker}_stock_data.json")
        with open(stock_data_path, "w") as f:
            json.dump(stock_data, f)
        print(f"Stock data saved to {stock_data_path}")
    except Exception as e:
        print(f"Error fetching stock chart data: {e}")
        # Decide whether to exit or continue; for now, let's exit if critical data is missing
        sys.exit(1)

    # Fetch Stock Insights Data
    try:
        print(f"Fetching stock insights data for {ticker}...")
        stock_insights = api_client.get_stock_insights(ticker=ticker)
        stock_insights_path = os.path.join(output_dir, f"{ticker}_stock_insights.json")
        with open(stock_insights_path, "w") as f:
            json.dump(stock_insights, f)
        print(f"Stock insights saved to {stock_insights_path}")
    except Exception as e:
        print(f"Error fetching stock insights data: {e}")
        sys.exit(1)

    # Fetch Stock Holders Data
    try:
        print(f"Fetching stock holders data for {ticker}...")
        stock_holders = api_client.get_stock_holders(ticker=ticker)
        stock_holders_path = os.path.join(output_dir, f"{ticker}_stock_holders.json")
        with open(stock_holders_path, "w") as f:
            json.dump(stock_holders, f)
        print(f"Stock holders data saved to {stock_holders_path}")
    except Exception as e:
        print(f"Error fetching stock holders data: {e}")
        sys.exit(1)

    # --- Step 2: Perform Data Analysis ---
    try:
        print("Performing data analysis...")
        # Load stock data
        with open(stock_data_path, "r") as f:
            stock_data_json = json.load(f)
        
        meta_info = stock_data_json["chart"]["result"][0]["meta"]
        timestamps = stock_data_json["chart"]["result"][0]["timestamp"]
        ohlcv = stock_data_json["chart"]["result"][0]["indicators"]["quote"][0]
        
        df = pd.DataFrame({
            "timestamp": pd.to_datetime(timestamps, unit="s"),
            "open": ohlcv["open"],
            "high": ohlcv["high"],
            "low": ohlcv["low"],
            "close": ohlcv["close"],
            "volume": ohlcv["volume"]
        })
        df.set_index("timestamp", inplace=True)
        df.dropna(inplace=True)

        # Calculate Moving Averages
        df["MA5"] = df["close"].rolling(window=5).mean()
        df["MA20"] = df["close"].rolling(window=20).mean()
        df["MA60"] = df["close"].rolling(window=60).mean()
        df["MA120"] = df["close"].rolling(window=120).mean()
        df["VolumeMA20"] = df["volume"].rolling(window=20).mean()

        # Technical Analysis Results
        latest_close = df["close"].iloc[-1]
        latest_ma5 = df["MA5"].iloc[-1]
        latest_ma20 = df["MA20"].iloc[-1]
        latest_ma60 = df["MA60"].iloc[-1]
        latest_ma120 = df["MA120"].iloc[-1]

        price_change_1m = (latest_close - df["close"].iloc[-20]) / df["close"].iloc[-20] * 100 if len(df) >= 20 else None
        price_change_3m = (latest_close - df["close"].iloc[-60]) / df["close"].iloc[-60] * 100 if len(df) >= 60 else None
        price_change_1y = (latest_close - df["close"].iloc[-252]) / df["close"].iloc[-252] * 100 if len(df) >= 252 else None # Assuming ~252 trading days in a year

        ma_status = {
            "MA5": "above" if latest_close > latest_ma5 else "below",
            "MA20": "above" if latest_close > latest_ma20 else "below",
            "MA60": "above" if latest_close > latest_ma60 else "below",
            "MA120": "above" if latest_close > latest_ma120 else "below",
        }

        trend = "upward" if latest_ma5 > latest_ma20 > latest_ma60 else "downward" if latest_ma5 < latest_ma20 < latest_ma60 else "sideways"
        
        # Load insights data
        with open(stock_insights_path, "r") as f:
            insights_result = json.load(f)

        support_resistance = insights_result.get("finance", {}).get("result", {}).get("instrumentInfo", {}).get("keyTechnicals", {})
        recommendations = insights_result.get("finance", {}).get("result", {}).get("recommendationTrend", {}).get("trend", [])
        key_developments = insights_result.get("finance", {}).get("result", {}).get("companySnapshot", {}).get("company", {}).get("hiring", []) # Example, adjust path as needed

        # Load stock holders data
        with open(stock_holders_path, "r") as f:
            stock_holders_data = json.load(f)
        
        major_holders = stock_holders_data.get("finance", {}).get("result", {}).get("majorHoldersBreakdown", {})
        insider_transactions = stock_holders_data.get("finance", {}).get("result", {}).get("insiderTransactions", {}).get("transactions", [])


        analysis_result = {
            "meta_info": meta_info,
            "current_price": latest_close,
            "price_changes": {
                "1_month_percentage": price_change_1m,
                "3_month_percentage": price_change_3m,
                "1_year_percentage": price_change_1y,
            },
            "moving_averages_status": ma_status,
            "current_trend": trend,
            "support_resistance": {
                "support": support_resistance.get("support"),
                "resistance": support_resistance.get("resistance"),
                "pivot": support_resistance.get("pivot") 
            },
            "analyst_recommendations": recommendations,
            "key_company_developments": key_developments,
            "major_shareholders": major_holders,
            "insider_transactions_summary": [t['filerName'] + ": " + t['transactionText'] for t in insider_transactions[:5]] # Top 5 transactions
        }
        
        # Comprehensive Analysis and Conclusion (Simplified example)
        conclusion = f"{ticker} is currently trading at {latest_close:.2f}. "
        conclusion += f"The current trend is {trend}, with the price {ma_status['MA20']} the 20-day MA. "
        if price_change_1m is not None:
            conclusion += f"Over the past month, the price has changed by {price_change_1m:.2f}%. "
        
        analysis_result["comprehensive_conclusion"] = conclusion

        analysis_result_path = os.path.join(output_dir, f"{ticker}_analysis_result.json")
        with open(analysis_result_path, "w") as f:
            json.dump(analysis_result, f, indent=4)
        print(f"Analysis results saved to {analysis_result_path}")

    except Exception as e:
        print(f"Error during data analysis: {e}")
        sys.exit(1)

    # --- Step 3: Generate Charts ---
    try:
        print("Generating charts...")
        # Load stock data for charting
        with open(stock_data_path, "r") as f:
            stock_data_for_charting_json = json.load(f)

        timestamps_chart = stock_data_for_charting_json["chart"]["result"][0]["timestamp"]
        ohlcv_chart = stock_data_for_charting_json["chart"]["result"][0]["indicators"]["quote"][0]

        df_chart = pd.DataFrame({
            "timestamp": pd.to_datetime(timestamps_chart, unit="s"),
            "open": ohlcv_chart["open"],
            "high": ohlcv_chart["high"],
            "low": ohlcv_chart["low"],
            "close": ohlcv_chart["close"],
            "volume": ohlcv_chart["volume"]
        })
        df_chart.set_index("timestamp", inplace=True)
        df_chart.dropna(inplace=True) # Drop rows with NaN values that can occur from rolling calculations

        # Recalculate MAs for charting on potentially different (fuller) dataset if df was modified
        df_chart["MA5"] = df_chart["close"].rolling(window=5).mean()
        df_chart["MA20"] = df_chart["close"].rolling(window=20).mean()
        df_chart["MA60"] = df_chart["close"].rolling(window=60).mean()
        df_chart["MA120"] = df_chart["close"].rolling(window=120).mean()
        df_chart["VolumeMA20"] = df_chart["volume"].rolling(window=20).mean()
        
        plt.style.use('seaborn-v0_8-darkgrid') # Using a seaborn style
        fig, axes = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})
        
        # Price Chart
        axes[0].plot(df_chart.index, df_chart["close"], label="Close Price", color="blue")
        axes[0].plot(df_chart.index, df_chart["MA20"], label="MA20", color="orange", linestyle="--")
        axes[0].plot(df_chart.index, df_chart["MA60"], label="MA60", color="green", linestyle="--")
        axes[0].set_title(f"{ticker} Stock Price and Moving Averages")
        axes[0].set_ylabel("Price (USD)") # Assuming USD, adjust if needed
        axes[0].legend()
        
        # Volume Chart
        axes[1].bar(df_chart.index, df_chart["volume"], label="Volume", color="grey", alpha=0.6)
        axes[1].plot(df_chart.index, df_chart["VolumeMA20"], label="Volume MA20", color="red", linestyle="--")
        axes[1].set_title(f"{ticker} Trading Volume")
        axes[1].set_ylabel("Volume")
        axes[1].set_xlabel("Date")
        axes[1].legend()
        
        plt.tight_layout()
        chart_path = os.path.join(output_dir, f"{ticker}_stock_chart.png")
        plt.savefig(chart_path)
        plt.close() # Close the plot to free up memory
        print(f"Stock chart saved to {chart_path}")

    except Exception as e:
        print(f"Error generating charts: {e}")
        # Decide if to exit or continue; for now, just print error and continue
        # sys.exit(1)

    # --- Step 4: Calculate Technical Indicators ---
    try:
        print("Calculating technical indicators...")
        # Load stock data for technical indicators
        with open(stock_data_path, "r") as f:
            stock_data_for_tech_json = json.load(f)

        timestamps_tech = stock_data_for_tech_json["chart"]["result"][0]["timestamp"]
        ohlcv_tech = stock_data_for_tech_json["chart"]["result"][0]["indicators"]["quote"][0]
        
        df_tech = pd.DataFrame({
            "timestamp": pd.to_datetime(timestamps_tech, unit="s"),
            "close": ohlcv_tech["close"]
        })
        df_tech.set_index("timestamp", inplace=True)
        df_tech.dropna(inplace=True)

        # RSI Calculation
        delta = df_tech["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df_tech["RSI"] = 100 - (100 / (1 + rs))

        # Bollinger Bands
        df_tech["MA20_BB"] = df_tech["close"].rolling(window=20).mean()
        df_tech["STD20_BB"] = df_tech["close"].rolling(window=20).std()
        df_tech["Upper_BB"] = df_tech["MA20_BB"] + (df_tech["STD20_BB"] * 2)
        df_tech["Lower_BB"] = df_tech["MA20_BB"] - (df_tech["STD20_BB"] * 2)

        # MACD
        df_tech["EMA12"] = df_tech["close"].ewm(span=12, adjust=False).mean()
        df_tech["EMA26"] = df_tech["close"].ewm(span=26, adjust=False).mean()
        df_tech["MACD"] = df_tech["EMA12"] - df_tech["EMA26"]
        df_tech["Signal_Line"] = df_tech["MACD"].ewm(span=9, adjust=False).mean()

        # Select last 30 days of indicators
        technical_indicators_df = df_tech[["RSI", "Upper_BB", "Lower_BB", "MACD", "Signal_Line"]].tail(30)
        
        technical_indicators_path = os.path.join(output_dir, f"{ticker}_technical_indicators.csv")
        technical_indicators_df.to_csv(technical_indicators_path)
        print(f"Technical indicators saved to {technical_indicators_path}")

    except Exception as e:
        print(f"Error calculating technical indicators: {e}")
        # sys.exit(1) # Decide if to exit or continue

    print("Stock analysis script completed.")

if __name__ == "__main__":
    main()
