


import os
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D
from keras.layers import Activation,Dropout,Flatten,Dense
from PIL import Image
import numpy as np




categories = ["chair","camera","butterfly","elephant","flamingo"]
nb_classes = len(categories)

image_w = 64
image_h = 64

data = np.load("./saveFiles/caltech_5object.npz")
X_train = data["X_train"]
X_test = data["X_test"]
Y_train = data["Y_train"]
Y_test = data["Y_test"]

X_train = X_train.astype("float") /256
X_test = X_test.astype("float") /256
print('X_train shape', X_train.shape)


model = Sequential()

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


# 모델 훈련 및 hdf5로 저장
# 모델 훈련 및 가중치를 파일로 저장하기
h5_file = "./saveFiles/caltech_5object_model.weights.h5"
if os.path.exists(h5_file):
    # 이미 존재하면 가중치 모델을 메모리에 로드
    model.load_weights(h5_file)
else:
    # 없으면 훈련을 진행한 후 결과를 가중치 모델로 저장한다.
    model.fit(X_train,Y_train,batch_size=32,epochs=50)
    model.save_weights(h5_file)
    
# 모델평가 : 테스트 데이터를 통해 예측
pre = model.predict(X_test)
# 평가된 결과 데이터를 통해 반복
for i,v in enumerate(pre):
    # 모델이 예측한 클래스를 통해 가장 확률이 높은 인덱스
    pre_ans = v.argmax()
    # 실제 정답 클래스중 가장 확률이 높은 인덱스
    ans = Y_test[i].argmax()
    # 원본 이미지 데이터
    dat = X_test[i]
    # 예측이 정답이면 반복문의 처음으로 돌아간다.
    if ans == pre_ans:
        # continue : 무조건 반복문의 처음으로 돌아간다.
        continue
    # 예측이 틀린 경우에는 NG 메시지를 출력한다.
    print("[NG]", categories[pre_ans], "!=", categories[ans])
    print(v)
    # 예측에 실패한 이미지 저장 경로 설정
    fname = "./predict_error/" + str(i) + "-"+ categories[pre_ans]+"-ne-"+categories[ans]+".png"
    # 0~1 범위의 이미지 데이터를 0~255로 변환
    dat *=256
    # 넘파이 배열을 이미지 객체로 변환후...
    img = Image.fromarray(np.uint8(dat))
    # 파일로 저쟝한다.
    img.save(fname)
    
score = model.evaluate(X_test,Y_test)

#손실출력
print('loss=',score[0])
#정확도출력
print('accuracy=',score[1])