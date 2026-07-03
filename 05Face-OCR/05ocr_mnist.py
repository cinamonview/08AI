from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras import utils

# 하이퍼 파라미터
IMAGE_W = 28
IMAGE_H = 28
CLASSES_CNT = 10

# DNN(Deep Neural Network, 심층신경망)을 이용한 모델
def main():
    (X_train, Y_train), (X_test, Y_test) = mnist.load_data()
    # 데이터를 1차원 배열로 변환
    X_train = (X_train.reshape(X_train.shape[0], IMAGE_W * IMAGE_H)
               .astype('float32'))
    X_test = (X_test.reshape(X_test.shape[0], IMAGE_W * IMAGE_H)
              .astype('float32'))
    # 데이터 정규화
    X_train /= 255
    X_test /= 255
    # 원-핫 인코딩(10개 클래스)
    Y_train = utils.to_categorical(Y_train, 10)
    Y_test = utils.to_categorical(Y_test, 10)
    # 모델 구축
    model = build_model()
    # 훈련
    model.fit(X_train, Y_train, batch_size=128, epochs=20, verbose=1,
              validation_data=(X_test, Y_test))
    # 학습된 모델 저장(가중치 포함)
    model.save('./saveFiles/mnist_model.h5')
    # 모델 평가
    score = model.evaluate(X_test, Y_test, verbose=0)
    print('score=', score)

def build_model():
    # MLP(Multilayer Perceptron, 다층 퍼셉트론) 모델 구축
    model = Sequential()
    # 첫 번째 은닉층
    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    # 두 번째 은닉층
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    # 출력층 (뉴런 10개, 클래스 개수와 동일)
    model.add(Dense(CLASSES_CNT))
    model.add(Activation('softmax'))
    # 모델 컴파일
    model.compile(loss='categorical_crossentropy',
                  optimizer=RMSprop(),
                  metrics=['accuracy'])
    return model

if __name__ == '__main__':
    main()

