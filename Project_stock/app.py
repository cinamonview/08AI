from flask import Flask, render_template, jsonify
import pymysql
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'stock_user',
    'password': 'stock1234',
    'db': 'stock_predict',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_historical_data(ticker):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5*365) # 과거 5년 전
    
    df = yf.download(ticker, start=start_date, end=end_date)
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        
    df = df.reset_index()
    df['Month'] = df['Date'].dt.to_period('M')
    
    monthly_avg = df.groupby('Month')['Close'].mean().reset_index()
    monthly_avg['Month'] = monthly_avg['Month'].astype(str)
    return monthly_avg

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/historical-vs-prediction/<ticker>')
def get_historical_vs_prediction(ticker):
    try:
        df_all = get_historical_data(ticker)

        # 1. 과거 5년 라벨 (60개월)
        all_labels = df_all['Month'].tolist()
        
        # 2. 미래 12개월 라벨 추가 생성 (총 72개월 만들기)
        last_month_str = all_labels[-1] # 과거 데이터의 마지막 달 (현재 달)
        last_date = datetime.strptime(last_month_str, '%Y-%m')
        
        for i in range(1, 13):
            # 한 달씩 더해가며 미래 년-월 문자열 생성
            future_date = last_date + pd.DateOffset(months=i)
            all_labels.append(future_date.strftime('%Y-%m'))
            
        # 오늘 기준 2년 전 년-월
        two_years_ago_str = (datetime.now() - timedelta(days=2*365)).strftime('%Y-%m')

        actual_72m = []       # 72개월 실제 주가 리스트 (미래 12개월은 빈칸)
        predicted_72m = []    # 72개월 예측 주가 리스트 (과거 최근2년 ~ 미래12개년만 채움)

        # 과거 60개월 데이터 먼저 채우기
        for _, row in df_all.iterrows():
            current_month = row['Month']
            current_price = row['Close']
            
            # 실제 주가는 과거 데이터만 채우고 끝남
            actual_72m.append(current_price)
            
            # 예측 주가는 최근 2년 구간부터 채우기 시작
            if current_month >= two_years_ago_str:
                predicted_72m.append(current_price * 1.05) # 임시 ML 백테스팅 예측치
            else:
                predicted_72m.append(None)

        # 미래 12개월 데이터 채우기 (실제 주가는 None, 예측 주가는 계속 이어짐)
        # 마지막 주가 기준으로 미래에 조금씩 우상향하는 임시 시나리오 적용
        base_price = df_all['Close'].iloc[-1] * 1.05
        for i in range(1, 13):
            actual_72m.append(None) # 미래의 실제 주가는 당연히 모르니까 None!
            
            # 미래 12개월 동안 서서히 상승하는 예측 그래프 생성
            future_predict_price = base_price * (1 + (i * 0.01)) 
            predicted_72m.append(future_predict_price)

        response_data = {
            'labels': all_labels,
            'actual_historical_5y': actual_72m,
            'predicted_2y_plus_future': predicted_72m
        }

        # 달러 환산 치트키 (애플)
        if ticker == 'AAPL':
            exchange_rate = 1400
            response_data['actual_historical_5y'] = [int(val * exchange_rate) if val is not None else None for val in response_data['actual_historical_5y']]
            response_data['predicted_2y_plus_future'] = [int(val * exchange_rate) if val is not None else None for val in response_data['predicted_2y_plus_future']]

        return jsonify(response_data)

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)