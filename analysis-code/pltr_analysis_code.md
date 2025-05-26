# 팔란티어(PLTR) 주가 분석에 사용된 Python 코드

## 1. 주가 데이터 수집 코드

다음 코드는 Yahoo Finance API를 통해 팔란티어(PLTR)의 주가 데이터를 수집하는 데 사용되었습니다:

```python
import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient
import json

# API 클라이언트 초기화
client = ApiClient()

# 팔란티어(PLTR) 주가 차트 데이터 가져오기
stock_data = client.call_api('YahooFinance/get_stock_chart', query={
    'symbol': 'PLTR',
    'region': 'US',
    'interval': '1d',
    'range': '1y',
    'includeAdjustedClose': True
})

# 결과를 JSON 파일로 저장
with open('pltr_stock_data.json', 'w') as f:
    json.dump(stock_data, f, indent=2)

print("팔란티어 주가 데이터가 pltr_stock_data.json 파일에 저장되었습니다.")
```

## 2. 주가 인사이트 데이터 수집 코드

다음 코드는 Yahoo Finance API를 통해 팔란티어(PLTR)의 인사이트 데이터를 수집하는 데 사용되었습니다:

```python
import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient
import json

# API 클라이언트 초기화
client = ApiClient()

# 팔란티어(PLTR) 인사이트 데이터 가져오기
stock_insights = client.call_api('YahooFinance/get_stock_insights', query={
    'symbol': 'PLTR'
})

# 결과를 JSON 파일로 저장
with open('pltr_stock_insights.json', 'w') as f:
    json.dump(stock_insights, f, indent=2)

print("팔란티어 인사이트 데이터가 pltr_stock_insights.json 파일에 저장되었습니다.")
```

## 3. 주주 및 내부자 거래 데이터 수집 코드

다음 코드는 Yahoo Finance API를 통해 팔란티어(PLTR)의 주주 및 내부자 거래 데이터를 수집하는 데 사용되었습니다:

```python
import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient
import json

# API 클라이언트 초기화
client = ApiClient()

# 팔란티어(PLTR) 주주 데이터 가져오기
stock_holders = client.call_api('YahooFinance/get_stock_holders', query={
    'symbol': 'PLTR',
    'region': 'US'
})

# 결과를 JSON 파일로 저장
with open('pltr_stock_holders.json', 'w') as f:
    json.dump(stock_holders, f, indent=2)

print("팔란티어 주주 데이터가 pltr_stock_holders.json 파일에 저장되었습니다.")
```

## 4. 주가 데이터 분석 및 결과 추출 코드

다음 코드는 수집된 데이터를 분석하고 주요 지표를 계산하는 데 사용되었습니다:

```python
import json
import pandas as pd
from datetime import datetime

# 주가 데이터 로드
with open('pltr_stock_data.json', 'r') as f:
    stock_data = json.load(f)

# 인사이트 데이터 로드
with open('pltr_stock_insights.json', 'r') as f:
    stock_insights = json.load(f)

# 주주 데이터 로드
with open('pltr_stock_holders.json', 'r') as f:
    stock_holders = json.load(f)

# 메타 정보 추출
meta = stock_data['chart']['result'][0]['meta']
current_price = meta.get('regularMarketPrice', 'N/A')
week52_high = meta.get('fiftyTwoWeekHigh', 'N/A')
week52_low = meta.get('fiftyTwoWeekLow', 'N/A')
day_high = meta.get('regularMarketDayHigh', 'N/A')
day_low = meta.get('regularMarketDayLow', 'N/A')
volume = meta.get('regularMarketVolume', 'N/A')
prev_close = meta.get('chartPreviousClose', 'N/A')

# 주가 데이터 추출 및 DataFrame 생성
result = stock_data['chart']['result'][0]
timestamps = result['timestamp']
quote = result['indicators']['quote'][0]
adjclose = result['indicators']['adjclose'][0]['adjclose'] if 'adjclose' in result['indicators'] else None

# 날짜 변환
dates = [datetime.fromtimestamp(ts) for ts in timestamps]

# 데이터프레임 생성
df = pd.DataFrame({
    'Date': dates,
    'Open': quote['open'],
    'High': quote['high'],
    'Low': quote['low'],
    'Close': quote['close'],
    'Volume': quote['volume'],
    'Adj_Close': adjclose if adjclose else quote['close']
})

# 결측값 처리
df = df.dropna()

# 이동평균선 계산
df['MA_20'] = df['Close'].rolling(window=20).mean()
df['MA_50'] = df['Close'].rolling(window=50).mean()
df['MA_200'] = df['Close'].rolling(window=200).mean()

# 거래량 이동평균
df['Volume_MA_20'] = df['Volume'].rolling(window=20).mean()

# 기술적 분석 결과
latest_price = df['Close'].iloc[-1]
previous_price = df['Close'].iloc[-2]
price_change = latest_price - previous_price
price_change_pct = (price_change / previous_price) * 100
ma_20_latest = df['MA_20'].iloc[-1]
ma_50_latest = df['MA_50'].iloc[-1]
ma_200_latest = df['MA_200'].iloc[-1]
volume_latest = df['Volume'].iloc[-1]
volume_ma_20 = df['Volume_MA_20'].iloc[-1]
volume_change = (volume_latest / volume_ma_20 - 1) * 100

# 이동평균선 골든크로스/데드크로스 확인
ma_cross_status = ''
if ma_20_latest > ma_50_latest and df['MA_20'].iloc[-20] < df['MA_50'].iloc[-20]:
    ma_cross_status = '최근 20일/50일 이동평균선 골든크로스 발생 (단기 상승세)'
elif ma_20_latest < ma_50_latest and df['MA_20'].iloc[-20] > df['MA_50'].iloc[-20]:
    ma_cross_status = '최근 20일/50일 이동평균선 데드크로스 발생 (단기 하락세)'

ma_long_cross_status = ''
if ma_50_latest > ma_200_latest and df['MA_50'].iloc[-50] < df['MA_200'].iloc[-50]:
    ma_long_cross_status = '최근 50일/200일 이동평균선 골든크로스 발생 (장기 상승세)'
elif ma_50_latest < ma_200_latest and df['MA_50'].iloc[-50] > df['MA_200'].iloc[-50]:
    ma_long_cross_status = '최근 50일/200일 이동평균선 데드크로스 발생 (장기 하락세)'

# 추세 판단
trend = '중립'
if latest_price > ma_20_latest and ma_20_latest > ma_50_latest:
    trend = '강한 상승'
elif latest_price > ma_20_latest:
    trend = '상승'
elif latest_price < ma_20_latest and ma_20_latest < ma_50_latest:
    trend = '강한 하락'
elif latest_price < ma_20_latest:
    trend = '하락'

# 기술적 지표 정보
support_level = 'N/A'
resistance_level = 'N/A'
stop_loss = 'N/A'

if 'instrumentInfo' in insights_result and 'keyTechnicals' in insights_result['instrumentInfo']:
    key_tech = insights_result['instrumentInfo']['keyTechnicals']
    support_level = key_tech.get('support', 'N/A')
    resistance_level = key_tech.get('resistance', 'N/A')
    stop_loss = key_tech.get('stopLoss', 'N/A')

# 추천 정보
target_price = 'N/A'
provider = 'N/A'
rating = 'N/A'

if 'recommendation' in insights_result:
    recommendation = insights_result['recommendation']
    target_price = recommendation.get('targetPrice', 'N/A')
    provider = recommendation.get('provider', 'N/A')
    rating = recommendation.get('rating', 'N/A')

# 주요 개발 사항
sig_devs = []
if 'sigDevs' in insights_result and insights_result['sigDevs']:
    for dev in insights_result['sigDevs'][:3]:  # 최대 3개만 추출
        sig_devs.append({
            'date': dev.get('date', '날짜 정보 없음'),
            'headline': dev.get('headline', '정보 없음')
        })

# 내부자 거래 정보
insider_info = []
try:
    holders_result = stock_holders['quoteSummary']['result'][0]
    
    if 'insiderHolders' in holders_result:
        insider_holders = holders_result['insiderHolders']
        
        if 'holders' in insider_holders:
            for holder in insider_holders['holders'][:3]:  # 최대 3개만 추출
                name = holder.get('name', '이름 정보 없음')
                relation = holder.get('relation', '관계 정보 없음')
                transaction = holder.get('transactionDescription', '거래 정보 없음')
                
                # 날짜 정보 처리
                latest_trans_date = '날짜 정보 없음'
                if 'latestTransDate' in holder and 'fmt' in holder['latestTransDate']:
                    latest_trans_date = holder['latestTransDate']['fmt']
                
                # 보유 수량 처리
                position = '보유 수량 정보 없음'
                if 'positionDirect' in holder and 'fmt' in holder['positionDirect']:
                    position = holder['positionDirect']['fmt']
                
                insider_info.append({
                    'name': name,
                    'relation': relation,
                    'transaction': transaction,
                    'date': latest_trans_date,
                    'position': position
                })
except Exception as e:
    pass

# 종합 분석 및 결론
trend_analysis = ''
if trend in ['강한 상승', '상승']:
    trend_analysis = '최근 종가가 20일 이동평균선 위에 위치하고 있어 단기적으로 상승 모멘텀이 유지되고 있습니다.'
elif trend in ['강한 하락', '하락']:
    trend_analysis = '최근 종가가 20일 이동평균선 아래에 위치하고 있어 단기적으로 하락 압력이 존재합니다.'
else:
    trend_analysis = '최근 종가가 20일 이동평균선 부근에서 등락을 반복하며 방향성을 탐색 중입니다.'

volume_analysis = ''
if volume_latest > volume_ma_20 * 1.5:
    volume_analysis = '최근 거래량이 20일 평균 대비 크게 증가했습니다. 이는 시장 참여자들의 관심이 높아졌음을 의미하며, 주가 움직임의 신뢰도를 높여줍니다.'
elif volume_latest < volume_ma_20 * 0.5:
    volume_analysis = '최근 거래량이 20일 평균 대비 크게 감소했습니다. 이는 시장 참여자들의 관심이 줄어들었음을 의미하며, 현재 추세의 지속성에 의문을 제기합니다.'
else:
    volume_analysis = '최근 거래량은 20일 평균과 유사한 수준을 유지하고 있어, 시장 참여도는 안정적인 상태입니다.'

investment_opinion = ''
try:
    if rating != 'N/A':
        rating_lower = rating.lower()
        if 'buy' in rating_lower or 'strong buy' in rating_lower:
            investment_opinion = f'투자 분석가들은 팔란티어에 대해 **매수** 의견을 제시하고 있습니다.'
            if target_price != 'N/A':
                upside = ((float(target_price) / latest_price) - 1) * 100
                investment_opinion += f' 목표가 ${target_price}는 현재가 대비 {upside:.2f}% 상승 여력을 나타냅니다.'
        elif 'sell' in rating_lower or 'strong sell' in rating_lower:
            investment_opinion = f'투자 분석가들은 팔란티어에 대해 **매도** 의견을 제시하고 있습니다.'
            if target_price != 'N/A':
                downside = ((float(target_price) / latest_price) - 1) * 100
                investment_opinion += f' 목표가 ${target_price}는 현재가 대비 {downside:.2f}% 하락 가능성을 나타냅니다.'
        else:
            investment_opinion = f'투자 분석가들은 팔란티어에 대해 **중립** 의견을 제시하고 있습니다.'
    else:
        # 기술적 분석 기반 자체 의견
        if trend in ['강한 상승', '상승'] and volume_latest > volume_ma_20:
            investment_opinion = '기술적 분석 기준으로 단기적인 매수 기회가 있을 수 있으나, 투자 결정 전 추가적인 펀더멘털 분석이 권장됩니다.'
        elif trend in ['강한 하락', '하락'] and volume_latest > volume_ma_20:
            investment_opinion = '기술적 분석 기준으로 단기적인 매도 신호가 감지되며, 투자자들은 손절매 수준을 설정하는 것이 좋습니다.'
        else:
            investment_opinion = '현재 주가는 명확한 방향성을 보이지 않고 있어, 추가적인 시그널이 나타날 때까지 관망하는 것이 권장됩니다.'
except:
    investment_opinion = '투자 의견 분석 중 오류가 발생했습니다.'

# 결과를 JSON으로 저장
analysis_result = {
    'basic_info': {
        'company_name': meta.get('longName', '팔란티어 테크놀로지스'),
        'symbol': meta.get('symbol', 'PLTR'),
        'exchange': meta.get('fullExchangeName', 'Nasdaq'),
        'currency': meta.get('currency', 'USD')
    },
    'current_price': {
        'price': current_price,
        'week52_high': week52_high,
        'week52_low': week52_low,
        'day_high': day_high,
        'day_low': day_low,
        'volume': volume,
        'prev_close': prev_close,
        'price_change': f'{price_change:.2f}',
        'price_change_pct': f'{price_change_pct:.2f}'
    },
    'technical_analysis': {
        'ma_20': f'{ma_20_latest:.2f}',
        'ma_50': f'{ma_50_latest:.2f}',
        'ma_200': f'{ma_200_latest:.2f}',
        'ma_cross_status': ma_cross_status,
        'ma_long_cross_status': ma_long_cross_status,
        'trend': trend,
        'support_level': support_level,
        'resistance_level': resistance_level,
        'stop_loss': stop_loss
    },
    'volume_analysis': {
        'volume_latest': f'{volume_latest:,.0f}',
        'volume_ma_20': f'{volume_ma_20:,.0f}',
        'volume_change_pct': f'{volume_change:.2f}',
        'volume_analysis': volume_analysis
    },
    'investment_recommendation': {
        'target_price': target_price,
        'provider': provider,
        'rating': rating,
        'investment_opinion': investment_opinion
    },
    'key_developments': sig_devs,
    'insider_trading': insider_info,
    'conclusion': {
        'trend': trend,
        'trend_analysis': trend_analysis,
        'volume_analysis': volume_analysis,
        'investment_opinion': investment_opinion
    }
}

# JSON으로 저장
with open('pltr_analysis_result.json', 'w') as f:
    json.dump(analysis_result, f, indent=2)

print('분석 결과가 pltr_analysis_result.json 파일에 저장되었습니다.')
```

## 5. 데이터 시각화 코드 (차트 생성)

다음 코드는 수집된 데이터를 시각화하는 데 사용되었습니다:

```python
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

# 주가 데이터 로드
with open('pltr_stock_data.json', 'r') as f:
    stock_data = json.load(f)

# 주가 데이터 추출 및 DataFrame 생성
result = stock_data['chart']['result'][0]
timestamps = result['timestamp']
quote = result['indicators']['quote'][0]
adjclose = result['indicators']['adjclose'][0]['adjclose'] if 'adjclose' in result['indicators'] else None

# 날짜 변환
dates = [datetime.fromtimestamp(ts) for ts in timestamps]

# 데이터프레임 생성
df = pd.DataFrame({
    'Date': dates,
    'Open': quote['open'],
    'High': quote['high'],
    'Low': quote['low'],
    'Close': quote['close'],
    'Volume': quote['volume'],
    'Adj_Close': adjclose if adjclose else quote['close']
})

# 결측값 처리
df = df.dropna()

# 이동평균선 계산
df['MA_20'] = df['Close'].rolling(window=20).mean()
df['MA_50'] = df['Close'].rolling(window=50).mean()
df['MA_200'] = df['Close'].rolling(window=200).mean()

# 주가 차트 생성
plt.figure(figsize=(14, 8))

# 주가 및 이동평균선 그래프
plt.subplot(2, 1, 1)
plt.plot(df['Date'], df['Close'], label='종가', color='black')
plt.plot(df['Date'], df['MA_20'], label='20일 이동평균선', color='blue')
plt.plot(df['Date'], df['MA_50'], label='50일 이동평균선', color='orange')
plt.plot(df['Date'], df['MA_200'], label='200일 이동평균선', color='red')
plt.title('팔란티어(PLTR) 주가 및 이동평균선')
plt.ylabel('주가 (USD)')
plt.grid(True, alpha=0.3)
plt.legend()

# 거래량 그래프
plt.subplot(2, 1, 2)
plt.bar(df['Date'], df['Volume'], color='green', alpha=0.5)
plt.title('팔란티어(PLTR) 거래량')
plt.ylabel('거래량')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('pltr_stock_chart.png', dpi=300)
plt.close()

print('팔란티어 주가 차트가 pltr_stock_chart.png 파일로 저장되었습니다.')
```

## 6. 기술적 지표 계산 코드

다음 코드는 추가적인 기술적 지표를 계산하는 데 사용되었습니다:

```python
import pandas as pd
import numpy as np
import json
from datetime import datetime

# 주가 데이터 로드
with open('pltr_stock_data.json', 'r') as f:
    stock_data = json.load(f)

# 주가 데이터 추출 및 DataFrame 생성
result = stock_data['chart']['result'][0]
timestamps = result['timestamp']
quote = result['indicators']['quote'][0]
adjclose = result['indicators']['adjclose'][0]['adjclose'] if 'adjclose' in result['indicators'] else None

# 날짜 변환
dates = [datetime.fromtimestamp(ts) for ts in timestamps]

# 데이터프레임 생성
df = pd.DataFrame({
    'Date': dates,
    'Open': quote['open'],
    'High': quote['high'],
    'Low': quote['low'],
    'Close': quote['close'],
    'Volume': quote['volume'],
    'Adj_Close': adjclose if adjclose else quote['close']
})

# 결측값 처리
df = df.dropna()

# 이동평균선 계산
df['MA_20'] = df['Close'].rolling(window=20).mean()
df['MA_50'] = df['Close'].rolling(window=50).mean()
df['MA_200'] = df['Close'].rolling(window=200).mean()

# 상대강도지수(RSI) 계산
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

df['RSI_14'] = calculate_rsi(df['Close'])

# 볼린저 밴드 계산
def calculate_bollinger_bands(data, window=20, num_std=2):
    ma = data.rolling(window=window).mean()
    std = data.rolling(window=window).std()
    upper_band = ma + (std * num_std)
    lower_band = ma - (std * num_std)
    
    return upper_band, ma, lower_band

df['BB_Upper'], df['BB_Middle'], df['BB_Lower'] = calculate_bollinger_bands(df['Close'])

# MACD 계산
def calculate_macd(data, fast=12, slow=26, signal=9):
    ema_fast = data.ewm(span=fast, adjust=False).mean()
    ema_slow = data.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram

df['MACD_Line'], df['MACD_Signal'], df['MACD_Histogram'] = calculate_macd(df['Close'])

# 기술적 지표 결과 저장
technical_indicators = df[['Date', 'Close', 'MA_20', 'MA_50', 'MA_200', 
                           'RSI_14', 'BB_Upper', 'BB_Middle', 'BB_Lower',
                           'MACD_Line', 'MACD_Signal', 'MACD_Histogram']].tail(30)

# CSV 파일로 저장
technical_indicators.to_csv('pltr_technical_indicators.csv', index=False)

print('팔란티어 기술적 지표가 pltr_technical_indicators.csv 파일로 저장되었습니다.')
```

이 코드들은 팔란티어 주가 분석을 위해 데이터 수집, 처리, 분석, 시각화 등의 과정에서 사용되었습니다. 각 코드는 특정 목적에 맞게 설계되었으며, 필요에 따라 수정하여 다른 주식 분석에도 활용할 수 있습니다.
