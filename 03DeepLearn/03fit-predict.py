import tensorflow as tf
import numpy as np

# 입력데이터 x를 2차원 배열로 정의. 자료형은 실수. 
x = np.array([[1.], [2.], [3.], [4.]], dtype=np.float32)
# 정답데이터 y=2x의 관계를 학습하도록 구성. 
y = np.array([[2.], [4.], [6.], [8.]], dtype=np.float32)

# Sequential 모델 생성. 노드가 1개인 완전연결층 사용함. 
model = tf.keras.Sequential([
    tf.keras.layers.Dense(1, input_shape=(1,))
])
# 모델을 학습 가능하도록 컴파일. 활성화함수, 손실함수 지정. 
model.compile(optimizer="sgd", loss="mse")
''' 
모델의 학습 수행. x는 입력데이터, y는 레이블데이터
epochs : 학습시 반복 횟수 '''
model.fit(x, y, epochs=40, verbose=1)
'''
학습된 모델에 새로운 입력값 5를 넣어서 예측을 수행해본다. 
결과가 10에 가까우면 모델이 정상적으로 학습된것으로 판단할 수 있다. 
(10~50까지 epochs를 조절하면서 테스트) 
'''
print(model.predict(np.array([[5.]], dtype=np.float32)))






