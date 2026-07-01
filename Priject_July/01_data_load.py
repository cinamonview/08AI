from datetime import datetime
import os
import pandas as pd
import yfinance as tf_finance

# 🌟 [추가] 오늘 날짜를 'YYYY-MM-DD' 형식의 문자열로 자동으로 가져옵니다.
today = datetime.today().strftime('%Y-%m-%d')

# 현재 이 파이썬 파일이 있는 진짜 위치(폴더 경로)를 알아냅니다.
base_path = os.path.dirname(os.path.abspath(__file__))

# 그 파일 위치 바로 아래에 'resData'를 붙여서 최종 경로를 만듭니다.
folder_path = os.path.join(base_path, 'resData')

# 만약 그 경로에 폴더가 없으면 새로 생성!
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"👉 파일과 같은 위치에 '{folder_path}' 폴더를 생성했습니다.")

# 1. 삼성전자 데이터 가져오기 (종료일을 오늘 날짜 변수인 today로 변경)
print(f"삼성전자 데이터 다운로드 중... (기준일: {today})")
sam = tf_finance.download('005930.KS', start='2020-01-01', end=today)

# 2. 비트코인 데이터 가져오기 (종료일을 오늘 날짜 변수인 today로 변경)
print(f"비트코인 데이터 다운로드 중... (기준일: {today})")
btc = tf_finance.download('BTC-KRW', start='2020-01-01', end=today)

# 3. CSV 파일로 안전하게 저장하기
sam.to_csv(os.path.join(folder_path, 'samsung.csv'))
btc.to_csv(os.path.join(folder_path, 'bitcoin.csv'))
print(f"\n저장 완료! '{folder_path}' 폴더를 확인해보세요.")