


from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D
from keras.layers import Activation,Dropout,Flatten,Dense
import numpy as np

# 카테고리 지정 : 분류할 대상 클래스 목록을 5개로 설정
categories = ["chair","camera","butterfly","elephant","flamingo"]
nb_classes = len(categories)

# 이미지 크기 지정
# 리사이즈 이미지 사이즈
image_w = 64
image_h = 64

# NPZ 파일 불러오기 (로드)
data = np.load("./saveFiles/caltech_5object.npz")
# savez() 함수로 저장시 이미 훈련용/테스트용 으로 분리함
X_train = data["X_train"]
X_test = data["X_test"]
Y_train = data["Y_train"]
Y_test = data["Y_test"]


# 학습 및 테스트 데이터 정규화
X_train = X_train.astype("float") /256
X_test = X_test.astype("float") /256

# 데이터 형태 출력( 샘플 갯수, 64,64,  채널수)
print('X_train shape', X_train.shape)

# 모델 생성
# 레이어를 순차적으로 쌓는 방식으로 훈련 모델 생성
model = Sequential()

# 입력층 : 첫번째 합성곱 (Convolution )층
'''
3*3 크기의 필터 32개를 적용하고 
padding : 출력크기를 동일하게 유지하는 same으로 설정
input_shape : 입력데이터 형태를 지정 (64*64*채널수)
'''

model.add(Conv2D(32,(3,3),padding='same', input_shape=X_train.shape[1:]))
# ReLU 활성화 함수 적용
model.add(Activation('relu'))
# 2*2 최대 풀링 적용
model.add(MaxPooling2D(pool_size=(2,2)))
# 과적합 방지를 위한 Dropout 적용 ( 25% 의 뉴런을 비활성화 한다.)
model.add(Dropout(0.25))


# 은닉층 1 : 두번째 합성곱 층

model.add(Conv2D(64,(3,3),padding='same'))
model.add(Activation('relu'))

# 은닉층 2: 세번째 합성곱 층
model.add(Conv2D(64,(3,3)))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

# 은닉층 3 : 완전 연결층 (Fully Connected Layer)
model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))

# 출력층 : 클래스의 갯수만큼 뉴런 생성
model.add(Dense(nb_classes))
# 다중 클래스 분류를 위한 소프트맥스 활성화 함수 지정.
model.add(Activation('softmax'))

# 손실 함수, 옵티마이저, 평가지표를 설정하여 모델 컴파일.
model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

# 모델 훈련 (학습 데이터 적용)
model.fit(X_train,Y_train,batch_size=32,epochs=50)

# 모델 평가
score = model.evaluate(X_test, Y_test)

# 손실 출력
print('loss = ', score[0])

# 정확도 출력
print('accuracy=', score[1])