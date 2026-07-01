import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# 1. 파일 경로 설정 (아까 배운 안전한 경로 치트키!)
base_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_path, 'resData', 'samsung.csv') # 예시로 삼성전자 먼저!

# 2. CSV 데이터 불러오기 (🌟 수정된 부분)
# yfinance가 만든 대용량 CSV의 상위 헤더 꼬임을 방지하기 위해 header=[0,1] 또는 skiprows를 상황에 맞게 처리합니다.
# 가장 확실한 방법은 판다스가 자동으로 타입을 추론하되, 첫 2줄이 헤더일 경우를 대비하는 것입니다.
df = pd.read_csv(csv_path, header=[0, 1], index_col=0)

# MultiIndex 헤더를 깔끔하게 단일화합니다. (예: ('Close', '005930.KS') -> 'Close')
df.columns = df.columns.get_level_values(0)

# 3. 텐서플로우가 공부할 'Close' 데이터만 쏙 빼내기 (🌟 수정된 부분)
# 혹시나 남아있을지 모를 문자열이나 빈 칸(NaN)을 지우고 순수 숫자 float 타입으로 변경합니다.
df = df.dropna()
price_data = df[['Close']].values.astype('float32')

# 4. 스케일링 (0과 1 사이로 가격 압축하기)
# 💡 최고가는 1, 최저가는 0이 되도록 비율을 맞춥니다.
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_prices = scaler.fit_transform(price_data)

print(f"압축 전 원본 주가(첫 3개): \n{price_data[:3]}")
print(f"압축 후 비율 주가(첫 3개): \n{scaled_prices[:3]}")
print("-" * 50)

# 5. 시계열 데이터 쪼개기 (윈도우 만들기)
# 💡 "최근 5일치 데이터를 보고 -> 그 다음날 주가를 맞추자!"
X = [] # 인공지능이 공부할 5일치 데이터들이 들어갈 방
y = [] # 인공지능이 맞춰야할 다음날 정답 데이터들이 들어갈 방

window_size = 5 # 5일치를 볼지, 20일치를 볼지 결정하는 숫자입니다.

for i in range(len(scaled_prices) - window_size):
    # i부터 i+5 직전까지 (0번째~4번째 날의 데이터)
    X.append(scaled_prices[i : i + window_size])
    # i+5번째 데이터 (5번째 날의 정답 데이터)
    y.append(scaled_prices[i + window_size])

# 컴퓨터가 계산하기 좋게 넘파이(Numpy) 행렬로 변환합니다.
X = np.array(X)
y = np.array(y)

print(f"전체 학습용 데이터 개수: {len(X)}개")
print(f"하나의 입력 데이터 형태 (5일치): \n{X[0]}")
print(f"그에 대응하는 내일 정답: {y[0]}")