import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# =================================================================
# 🌟 [여기만 수정하세요!] 원하는 자산을 지정하면 코드가 알아서 움직입니다.
# 삼성전자를 보고 싶을 때  -> 'samsung'
# 비트코인을 보고 싶을 때 -> 'bitcoin'
TARGET = 'samsung' 
# =================================================================

# 1. 파일 이름 및 출력 문구 자동 설정
target_name = "삼성전자" if TARGET == 'samsung' else "비트코인"
print(f"🎬 현재 {target_name} 데이터로 인공지능 학습을 준비합니다...")

base_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_path, 'resData', f'{TARGET}.csv')

# 2. 데이터 불러오기 및 전처리
df = pd.read_csv(csv_path, header=[0, 1], index_col=0)
df.columns = df.columns.get_level_values(0)
df = df.dropna()

price_data = df[['Close']].values.astype('float32')

# 스케일링
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_prices = scaler.fit_transform(price_data)

# 시계열 윈도우 쪼개기
X, y = [], []
window_size = 5

for i in range(len(scaled_prices) - window_size):
    X.append(scaled_prices[i : i + window_size])
    y.append(scaled_prices[i + window_size])

X = np.array(X)
y = np.array(y)

# 3. 텐서플로우 LSTM 모델 생성 및 학습
model = Sequential([
    LSTM(50, activation='tanh', input_shape=(window_size, 1)),
    Dense(1)
])
model.compile(optimizer='adam', loss='mean_squared_error')

print(f"🚀 {target_name} 학습 시작...")
model.fit(X, y, epochs=100, batch_size=32, verbose=1) # verbose=1로 학습 과정 출력
print("🎉 학습 완료!")

# 4. 내일 가격 예측하기
last_5_days = scaled_prices[-window_size:]
last_5_days = np.array([last_5_days])

pred_scaled = model.predict(last_5_days)
pred_price = scaler.inverse_transform(pred_scaled)

print("-" * 50)
print(f"🔮 인공지능이 예측한 내일의 {target_name} 예상 종가: {pred_price[0][0]:,.2f}원")
print("-" * 50)