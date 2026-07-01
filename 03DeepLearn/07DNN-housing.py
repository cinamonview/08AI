'''
DNN (DEeep Neural Network) :
    인간 두뇌의 뉴런과 시냅스 구조를 모방하여 만든 전산모델.
    초기에는 이산수학과 그래프 이론에서 아이디어를 얻어 개발됨.
    입력층, 은닉층, 출력층 으로 구성되며 각 층의 뉴런들이 연결되어 
    신호를 전달하고 처리함.
    ANN(인공신경망)의 한 종류로 은닉층의 갯수가 2개 이상인
    신경망을 의미한다
    Deep(심층)이라는 단어는 이러한 다수의 은닉층을 통해 복잡한 
    데이터의 비선형적 관계를 학습하고 표현하는 능력이
    뛰어남을 의미한다.
'''

# 시각화 관련 패키지
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from time import time

# Keras 관련 패키지 (딥러닝 모델 구현)
from keras.models import Sequential
from keras.layers import Dense

# 데이터 전처리 및 학습을 위한 패키지
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# 개별 실행을 위한 exit() 함수 사용.
import sys


# 하이퍼 파라미터
'''
모델이 학습하는 과정 자체를 제어하는 설정값을 의미한다.
학습전 사용자가 직접 설정해야 하며 모델 성능에 큰 영향을 미친다.
    -에포크(Epoch) : 전체 데이터셋이 신경망을 한번 통과하는
        학습 반복 횟수를 의미한다.
        즉 전체 데이터로 몇번 학습할지를 결정하는 값이다.
    -배치크기(Batch_size) : 전체 학습 데이터를 한번에 
        학습하는 것이 아닌 일정한 크기로 나눠서 처리하는데,
        이때 한번에 사용하는 데이터 샘플의 갯수를 의미한다.
'''
MY_EPOCH = 500
MY_BATCH = 64

'''
하이퍼 파라미터의 설정값이 적절하지 않으면....
    - 과적합(OverFitting) : 모델이 훈련 데이터에만 지나치게 
        맞춰져서 새로운 데이터에 대해 성능이 떨어지는 현상.
    - 과소적합(UnderFitting) : 모델이 훈련 데이터 조차
        제대로 학습하지 못해 전반적으로 낮은 성능을 보이는
        현상 등이 발생할 수 있다.
    그러니까 적절한 훈련량을 잘 찾아서 적절한 성능이 보일 수 있도록
    해야 한다.
'''

# 데이터의 컬럼명 지정
# 보스턴 집값 데이터셋으로 범죄율~ 집가격 까지로 구성되어있다.

heading = ['CRIM', 'ZN', 'INDUS', 'CHAS','NOX', 'RM', 'AGE',
           'DIS','RAD','TAX','PTRATIO', 'LSTAT','MEDV']

#CSV를 데이터 프레임으로 변환.
housing_df = pd.read_csv('resDATA/housing.csv')
print('데이터 샘플 10개')
print(housing_df.head(10))
print('데이터 통계')
print(housing_df.describe())
# sys.exit(0)

#Z-점수 정규화를 위한 객체 생성
'''
머신러닝 알고리즘은 데이터의 특정 패턴을 찾아 새로운 값을 예측한다.
서로 범위가 다른 데이터가 있을때 범위가 넓은 요소가 결과에 
더 큰 영향을 미치게 된다. 
이런 경우에 Z-점수 정규화가 필요하다.
'''
# 특정 패턴을 찾는게 머신러닝의 목표라고 할 수 있겠돠
scaler = StandardScaler()
# numpy의 ndarray로 변환
'''
데이터 프레임을 n차원 배열로 전환.
데이터 처리와 연산의 효율성을 위해 통일된 배열 형식을
사용하기 때문에 이와 같이 변환해준다.'''

Z_data = scaler.fit_transform(housing_df)
# 다시 데이터 프레임으로 변환하면서 컬럼을 추가한다.
Z_data = pd.DataFrame(Z_data, columns=heading)

print('정규화 된 데이터 샘플 10개')
print(Z_data.head(10))
print('정규화 된 데이터 통계')
print(Z_data.describe())
'''
변환 후 결과를 확인해 보면 mean(평균)은 0에 가까워지고
(-1.123388e-16 와 같이 e의 마이너스 16승) 
std(표준편차)는 1에 가까워진 것을 볼 수 있다.
(1.000990e+00 와 같이 e의 0승 이므로 거의 1에 가까움)
'''
# sys.exit(0)

# 입력(X)과 레이블 (Y) 데이터 분리 
# MEDV가 집값이다!!
# MEDV (주택가격) 컬럼은 학습용에서 제거하고, 평가용으로 사용한다.
X_data = Z_data.drop('MEDV', axis = 1)
# 레이블 데이터
Y_data = Z_data['MEDV']
X_train, X_test, Y_train,Y_test = train_test_split(X_data,Y_data, test_size=0.3)
print('\n 학습용 입력 데이터 모양:', X_train.shape)
print('학습용 레이블 데이터 모양:',Y_train.shape)
print('평가용 입력 데이터 모양:',X_test.shape)
print('평가용 레이블 데이터 모양:',Y_test.shape)

# 데이터 분포 확인을 위한 박스 플롯 출력
sns.set(font_scale=2)
sns.boxplot(data=Z_data, palette='dark')
plt.xticks(rotation=45) 
plt.show()

# sys.exit(0)

# DNN 인공신경망 구현(입력층, 은닉층 2개 , 출력층)
model = Sequential()
# 입력층의 노드수를 의미. 앞에서 주택가격을 제거했으므로 12개의 컬럼으로 구성되었다.
input_col = X_train.shape[1]
# 입력층과 첫번째 은닉층. input_dim에서 12개의 특성을 지정해준다.
# 뉴런 200개 , ReLu 활성화 함수 사용.
model.add(Dense(200,input_dim = input_col,activation='relu'))
# 두번째 은닉층. 뉴런 1000개, ReLU 활성화 함수 사용한다.
model.add(Dense(1000,activation='relu'))
# 출력층. 노드1개, 활성화 함수 지정이 없으므로 기본값인 선형함수를 사용한다.
model.add(Dense(1))
print('\nDNN 요약')
model.summary()

# sys.exit(0)
'''
요약설명 : 
    입력층과 은닉층1 사이 : 
        12개의 입력 노드와 200개의 은닉노드가 연결됨.
            - 총 시냅스 수 : 12 * 200 = 2400개
            - 각 시냅스마다 가중치(Weight) 1개씩 부여
            - 은닉층1 의 각 뉴런마다 바이어스(bias) 1개씩 존재 : 200개
            - 총 학습 파라미터 수 : 2,400 + 200 = 2,600개 
            
은닉층 1과 2 사이 : 200개의 은닉노드와 1000개의 은닉 노드가 연결됨
    - 가중치 : 200 * 1000 = 200,000개
    - 바이어스 : 1,000개
    - 총 학습 파라미터 수 : 201,000개
    
은닉층2와 출력층 사이 : 1000개의 은닉노드와 출력노드 1개 연결
    - 가중치 : 1,000개
    - 바이어스 : 1개
    - 총 학습 파라미터 수 : 1,001개
    
전체 학습 파라미터 : 2,600 + 201,000 + 1,001 = 204,601 개

파라미터(Parameter) : 인공신경망 모델이 학습을 통해 조정하는 값
가중치(Weight) : 각 연결(시냅스)에 존재하는 값의 크기로 입력값에 대해
    얼마나 영향을 미칠지를 결정하는 값
바이어스(Bias) : 각 뉴런이 고정적으로 가지는 편향값으로 입력이 
    모두 0 이어도 출력을 낼 수 있게 도와주는 값
'''


# 모델 학습을 위한 설정 : 최적화 함수와 손실 함수 지정
'''
optmizer : 최적화 함수
최적화함수 : 
    모델의 가중치를 얼마나, 어떻게 조정할지를 결정하는 함수.
    SGD는 확률적 경사하강법으로 일부 데이터(batch)를 사용해서
    조금씩 가중치를 갱신한다.
loss : 손실함수
손실함수 : 
    모델이 얼마나 잘못 예측했는지를 측정하는 기준으로, 모델의
    예측값과 실제값 사이의 차이를 수치로 나타내는 함수.
    딥러닝에서는 이 손실값을 줄이는 방향으로 모델을 학습한다.
    mse는 평균 제곱 오차를 의미한다.
'''

model.compile(optimizer='sgd', loss='mse')
# 학습 시작시간 기록
begin=time()
# 모델 학습 수행을 합니다.
model.fit(X_train, Y_train, epochs = MY_EPOCH, batch_size=MY_BATCH,verbose=1)
# verbose 훈련하는 과정을 터미널에서 볼것이냐.
# 종료시간 기록
end = time()
print('총 학습 시간 : {:.1f}초'.format(end - begin))

# 인공 신경망 평가 및 손실값 계산 (테스트용 데이터 사용)
'''
compile()함수에서 metrics를 추가하지 않았으므로,
loss(손실값) 하나만 반환된다.
즉 정확도는 반환되지 않는다.
'''

loss = model.evaluate(X_test,Y_test, verbose=1)
print('\nDNN 평균 제곱 오차 (MSE): {:.2f}'.format(loss))

#테스트 데이터로 예측 수행
pred = model.predict(X_test)

# 실제값 (Y_test)과 예측값(pred) 비교를 위한 회귀 그래프 출력
sns.regplot(x=Y_test, y=pred)
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.show()
