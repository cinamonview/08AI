# 케라스 사용을 위한 임포트 
from tensorflow.keras.datasets import mnist
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import utils

# MNIST 손글씨 데이터셋 로드 
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# 데이터 전처리
''' 
데이터를 float32로 변환하고 정규화한다. 28*28픽셀의 2차원 이미지를
784개의 1차원 배열로 변환하고, 훈련용 6만개, 테스트용 1만개로 분리. '''
X_train = X_train.reshape(60000, 784).astype('float32')
X_test  = X_test.reshape(10000, 784).astype('float32')
X_train /= 255
X_test  /= 255

# 원-핫 인코딩 형태로 변환 
''' 
정수형 레이블 데이터를 0~9까지의 카테고리를 나타내는 배열로 변환. 
즉 원-핫 인코딩 형태로 변환한다. Mnist는 손글씨 숫자를 표현한 데이터셋이다. '''
y_train = utils.to_categorical(y_train, 10)
y_test  = utils.to_categorical(y_test, 10)

# 모델 구조 정의 
#Sequential() : 모델의 각 레이어(층)을 순차적으로 추가하는 방식의 신경망 구성 
model = Sequential()
# 입력층 : 입력데이터는 784개의 1차원 배열로 설정 
''' 782개의 입력 신호를 받아 512개의 뉴런이 각장 복잡한 특징을 학습함. 여기서 512는 모델의 학습용량을 결정하는 하이퍼 파라미터. 숫자가 클수록 복잡한 패턴을 학습할 수 있다. 하지만 너무 크면 계산 속도가 느려지거나 과적합(Overfitting)이 발생할 수 있다.  '''
model.add(Dense(512, input_shape=(784,)))
# 활성화 함수 ReLU로 설정 
model.add(Activation('relu'))
# 과적합 방지를 위해 20%의 뉴런을 학습에서 제외 
model.add(Dropout(0.2))
# 은닉층 추가 
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.2))
# 출력층 추가. 활성화 함수로 softmax 사용 
model.add(Dense(10))
model.add(Activation('softmax'))

# 모델 컴파일
model.compile(
    loss='categorical_crossentropy',
    optimizer=Adam(),
    metrics=['accuracy'])

# 모델 학습
hist = model.fit(X_train, y_train)

# 테스트 데이터로 평가
score = model.evaluate(X_test, y_test, verbose=1)
print('loss=', score[0])
print('accuracy=', score[1])

