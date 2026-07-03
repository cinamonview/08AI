

from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D
from keras.layers import Activation,Dense,Dropout,Flatten
from keras import utils
import numpy as np

# 음식 이미지가 저장된 디렉토리와 카테고리 지정
# root_dir = "./download/"

categories = ["FriedChicken", "Kimchi", "MiyeokGuk", "Ramen", "Samgyeopsal"]
nb_classes = len(categories)
image_size = 224

# 데이터 로드 및 전처리 수행
'''
이 함수는 해당 파일을 직접 실행했을때만 호출되고,
다른 파일의 모듈로 임포트 될때는 호출되지 않는다.
'''
def main():
    #numpy 데이터 파일 불러오기
    data = np.load("./kfood/kfood_dataset.npz")
    X_train = data["X_train"]
    X_test = data["X_test"]
    Y_train = data["Y_train"]
    Y_test = data["Y_test"]
    
    # 데이터 정규화 하기 (0~1 범위로 조정) MinMAx 정규화
    X_train = X_train.astype("float")/ 256
    X_test = X_test.astype("float") /256
    # 레이블 데이터를 원-핫 인코딩으로 변환
    Y_train = utils.to_categorical(Y_train,nb_classes)
    Y_test = utils.to_categorical(Y_test,nb_classes)
    
    # 모델을 훈련하고 평가하기
    model = model_train(X_train,Y_train)
    model_eval(model,X_test,Y_test)
    
#CNN 모델 구축

def build_model(in_shape):
    # 모델 생성
    model = Sequential()
    # 입력층 : 첫번째 합성곱(Convolution )층
    model.add(Conv2D(32,3,3, padding='same',input_shape=in_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
    
    # 은닉층 1 : 두번째 합성곱 층
    model.add(Conv2D(64,3,3,padding='same'))
    model.add(Activation('relu'))
    
    #은닉층 2 : 세번째 합성곱 층
    model.add(Conv2D(64,3,3))
    model.add(MaxPooling2D(pool_size=(2,2), padding='same'))
    model.add(Dropout(0.25))
    
    #은닉층 3 : 완전 연결 층 (Fully Connected Layer)
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    
    # 출력층
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    # 모델 컴파일 : 손실 함수, 옵티마이저 , 평가지표
    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return model


# 모델훈련
def model_train(X,Y):
    #입력 데이터의 shape을 기반으로 모델 생성
    model = build_model(X.shape[1:])
    #모델 학습 수행
    model.fit(X,Y, batch_size=32, epochs= 30)
    # 모델 가중치 저장하기
    model.save_weights("./kfood/kfood_model.weights.h5")
    return model

# 테스트 데이터로 모델 평가
def model_eval(model,X,Y):
    score = model.evaluate(X,Y)
    # 손실값, 정확도 출력
    print('loss=', score[0])
    print('accuracy=', score[1])
    
    
if __name__ =="__main__":
    main()
