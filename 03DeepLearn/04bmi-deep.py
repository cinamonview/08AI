import tensorflow as tf
import pandas as pd
import numpy as np
import sys # exit() 함수 사용 

# BMI 데이터를 로드한 후 데이터프레임으로 변환 
csv = pd.read_csv("./resData/bmi.csv")

# 키와 몸무게를 Min-Max 정규화(최대값으로 나눠 0~1사이의 값을 변환) 
csv["height"] = csv["height"] / 200
csv["weight"] = csv["weight"] / 100

# label컬럼의 체형정보를 원-핫 인코딩 형태로 변환(딕셔너리로 정의)
bclass = {"thin": [1, 0, 0], "normal": [0, 1, 0], "fat": [0, 0, 1]}
# 기존 문자열(thin, normal등)을 변환 후 새로운 컬럼 생성 
csv["label_pat"] = csv["label"].apply(lambda x: np.array(bclass[x]))
# 데이터 중 상위 5개를 출력해서 확인 
print(csv.head())

'''
실행시 디버깅 혹은 결과확인을 해야하는 경우 실행을 멈추고 싶을때 
사용할 수 있는 함수 '''
# sys.exit(0)

# 테스트 데이터 분리 
test_csv = csv[15000:20000]
# 테스트용 입력 데이터(몸무게, 키 )
test_pat = np.array(test_csv[["weight", "height"]])
# 테스트용 정답 데이터(원-핫 인코딩)
test_ans = np.array(list(test_csv["label_pat"]))

''' 
신경망 모델 정의
  입력레이어 : 키와 몸무게 2개의 입력값 사용
  출력레이어 : 3개의 클래스(thin, normal, fat) 사용
    활성화함수는 softmax 사용 
'''
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(2,)),
    tf.keras.layers.Dense(3, activation='softmax')
])

# 훈련(학습)을 위한 모델 컴파일. 
#옵티마이저 : 확률적 경사하강법 / 손실함수 : 크로스 엔트로피 
model.compile(
    optimizer=tf.keras.optimizers.SGD(learning_rate=0.01),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 훈련용 데이터 준비 
train_pat = np.array(csv[["weight", "height"]])
train_ans = np.array(list(csv["label_pat"]))

# 모델 훈련 진행 
'''
epochs : 데이터셋 전체를 35번 반복 학습. 
batch_size : 학습 중 한번에 사용할 데이터 갯수 지정 
validation_data : 테스트 데이터를 사용해서 매 epochs마다 모델의
    성능을 검증함 
verbose : 훈련 진행 상황을 시각적으로 표시. 0이면 표시하지 않음. 
'''
history = model.fit(
    train_pat, train_ans,
    epochs=35,
    batch_size=100,
    validation_data=(test_pat, test_ans), # 테스트 데이터 검증
    verbose=1
)

# 평가 및 최종 정확도 출력. 
test_loss, test_acc = model.evaluate(test_pat, test_ans)
print("정답률 =", test_acc)


