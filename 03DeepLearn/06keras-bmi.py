from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.callbacks import EarlyStopping
import pandas as pd, numpy as np

# BMI 데이터 로드 후 데이터프레임으로 변환 
csv = pd.read_csv("./resData/bmi.csv")

# Min-Max 정규화 
csv["weight"] /= 100
csv["height"] /= 200
# 정규화된 키, 몸무게 컬럼을 입력데이터로 사용. 
X = csv[["weight", "height"]]

# 원-핫 인코딩 형식의 딕셔너리 생성 
bclass = {"thin":[1,0,0], "normal":[0,1,0], "fat":[0,0,1]}
''' 
행이 20000, 열이 3인 2차원 배열 생성. ones(), zeros() 함수와 
같이 배열을 생성할때 값을 채우지 않고, 빈값으로 배열을 생성함. '''
y = np.empty((20000,3))
# 2만개의 레이블 데이터를 bclass 형식으로 변환 
for i, v in enumerate(csv["label"]):
    y[i] = bclass[v]

# 훈련데이터 15000개, 테스트데이터 5000개로 분리
X_train, y_train = X[1:15001], y[1:15001]
X_test,  y_test  = X[15001:20001], y[15001:20001]

# 배열 형식으로 레이어 정의 후 모델 구조 정의
#각 층을 리스트에 추가하는 형식으로 add()함수 사용과 동일함. 
layers = [
    Dense(512, input_shape=(2,)),
    Activation('relu'),
    Dropout(0.1),
    Dense(512),
    Activation('relu'),
    Dropout(0.1),
    Dense(3),
    Activation('softmax')
]
model = Sequential(layers)

# 모델 컴파일. RMSprop 최적화 함수, 크로스엔트로피 손실 함수 적용.
model.compile(
    loss='categorical_crossentropy',
    optimizer="rmsprop",
    metrics=['accuracy'])

# 모델 학습
'''
batch_size : 한번에 100개씩 데이터를 묶어서 학습.
epochs : 학습 반복 횟수 
validation_split : 훈련데이터 중 10%를 검증 데이터로 사용. 
EarlyStopping : 조기종료
  monitor : 검증 손실값을 모니터링 함
  patience : 검증 손실값이 개선되지 않으면 학습을 x번 더 진행한 
    후 조기종료 하겠다는 옵션 
'''
hist = model.fit(
    X_train, y_train,
    batch_size=100,
    epochs=20,
    validation_split=0.1,
    callbacks=[EarlyStopping(monitor='val_loss', patience=2)],
    verbose=1)

# 테스트 데이터로 평가 
score = model.evaluate(X_test, y_test)
print('loss=', score[0])
print('accuracy=', score[1])





