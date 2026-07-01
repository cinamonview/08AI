'''
RNN(REcurrent Neural Network : 순환신경망 )
    순차적인 데이터(시간 순서가 있는 시계열 데이터)를 처리하기 
    위해 만들어진 딥러닝 모델. 문장, 음성, 주식, 센서데이터 등
    시간의 흐름이 중요한 데이터 학습에 사용된다.
    RNN은 일반 신경망과 달리 이전 시점의 정보를 '기억'해서 
    다음 시점의 계산에 반영한다. 
    즉 과거의 출력이 현재의 입력처리에 영향을 미친다.


'''


# 파이썬 패키지 임포트

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from time import time
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import InputLayer, Dense
'''
시간이 많이 지난 정보는 잘 기억하지 못하는 문제를 해결하기 위해 
등장한 변형 모델로 Long Short-Term Memory의 줄임말이다...
'''

from keras.layers import LSTM
import sys


#하이퍼 파라미터

MY_PAST = 12 # 과거 12개의 데이터를 입력으로 사용
MY_SPLIT = 0.8 # 학습데이터와 평가데이터 분할 비율
MY_UNIT = 300 #LSTM 유닛 갯수
# 입력데이터의 형태(12개의 시계열데이터, 1개의 특징)
MY_SHAPE = (MY_PAST,1) 
MY_EPOCH = 300
MY_BATCH = 64
# 출력시 소수점 3자리 까지 표시
np.set_printoptions(precision=3)

#CSV 파일을 데이터프레임으로 변환. header가 없으므로 모든 데이터를 변환한다.
# 1열 즉 탑승인원만 사용한다.
raw = pd.read_csv('resData/airline.csv', header=None, usecols=[1])

# 시계열 데이터 시각화

plt.plot(raw)
plt.show()

# 데이터 원본 출력
print('\n원본 데이터 샘플 13개')
print(raw.head(13))
print('\n정규화 데이터 통계')
print(raw.describe())  

# MinMax 데이터 정규화fh 0~1 사이로 변환
scaler = MinMaxScaler()
s_data = scaler.fit_transform(raw)
print('\nMinMax 정규화 형식 : ', type(s_data))

# 정규화 데이터 출력해보기
df = pd.DataFrame(s_data)
print('\n 정규화 데이터 샘플 13개')
print(df.head(13))
print('\n 정규화 데이터 통계')
print(df.describe())
# sys.exit(0)

# 13개 묶음으로 데이터 분할해서 리스트로 생성. 결과는 python 리스트
# 입력 12개 + 출력 1개

bundle = []
for i in range(len(s_data) - MY_PAST):
    bundle.append(s_data[i : i+MY_PAST+1])

# 데이터 분할 결과 확인
print('\n 총 13개 묶음의 수:', len(bundle))
print(bundle[0])
print(bundle[1])
# sys.exit(0)

# numpy로 전환
print('분할 데이터의 타입 : ', type(bundle))
bundle=np.array(bundle)
print('분할 데이터의 모양 : ', bundle.shape )

# 데이터를 입력과 출력으로 분할
# 첫 12개 데이터를 입력데이터(X)로 사용을 하고
X_data = bundle[:,0:MY_PAST]
# 마지막 데이터를 출력데이터(Y)로 사용해준다.
Y_data = bundle[:,-1]

# 데이터를 학습용과 평가용으로 분할
split = int(len(bundle)*MY_SPLIT)
X_train = X_data[: split]
X_test = X_data[split:]
Y_train = Y_data[: split]
Y_test = Y_data[split:]

# 최종 데이터 모양
print('\n 학습용 입력 데이터 모양 : ', X_train.shape)
print('학습용 레이블 데이터 모양 : ',Y_train.shape)
print('평가용 입력 데이터 모양 : ',X_test.shape)
print('평가용 레이블 데이터 모양 : ', Y_test.shape)
    
      
############## 인공 신경망 구현 ####################

# RNN구현(케라스 RNN은 2차원 입력만 허용)

model = Sequential()
# 입력층 설정(12개의 시계열 데이터, 1개 특징)
model.add(InputLayer(input_shape=MY_SHAPE))
# LSTM 레이어 추가. 300개의 유닛으로 시계열 학습
model.add(LSTM(MY_UNIT))

# 출력층
model.add(Dense(1, activation='sigmoid'))
print('\nRNN 요약')
# 모델의 층별로 출력형태와 파라미터수 확인
model.summary()
# sys.exit(0)

############# 인공 신경망 학습 ############

#최적화 함수와 손실 함수 지정
model.compile(optimizer='rmsprop',loss='mse')
begin = time()
print('\nRNN 학습시작')
# 모델 훈련
model.fit(X_train,Y_train, epochs=MY_EPOCH,batch_size=MY_BATCH,verbose=1)
end=time()
print('총 학습 시간 : {:.1f}초'.format(end - begin))   


####################### 인공 신경망 평가 ######################

# RNN 평가
loss = model.evaluate(X_test,Y_test, verbose=0)
print('최종 MSE 손실값 : {:.3f}'.format(loss))

# RNN 추측

pred = model.predict(X_test)
# 원래값으로 복원.
pred = scaler.inverse_transform(pred)
# 1차원 배열로 변환 및 정수형으로 변환
pred = pred.flatten().astype(int)
print('\n추측 결과 원본 : ',pred)


# 정답 역전환
# 정답 데이터 역전환. 즉 정규화된것을 1차원 정수형으로 변환.
truth = scaler.inverse_transform(Y_test)
truth = truth.flatten().astype(int)
print('\n정답 원본 : ', truth)

# 선 그래프로 시각화
axes = plt.gca()
axes.set_ylim([0,650])
# 예측 결과를 선으로 표시(파란색)
sns.lineplot(data=pred, label='pred',color='blue')
# 실제 결과는 빨간색 선으로 표시
sns.lineplot(data=truth, label='truth', color='red')
plt.show()