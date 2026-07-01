# 텐서플로우 모듈 임포트
import tensorflow as tf

# 1행2열인 실수 텐서 생성(입력데이터 역할)
x = tf.constant([[1.0, 2.0]])
# 2행1열인 실수 텐서(가중치 혹은 변환행렬의 역할)
y = tf.constant([[3.0], [4.0]])
# 자동미분을 기록하는 컨텍스트 생성 
with tf.GradientTape() as tape:
    # x를 미분 대상 변수로 등록
    tape.watch(x)
    # 행렬곱 연산 수행(1*3 + 2*4 = 11)
    z = tf.matmul(x, y)
# z를 x에 대해 미분한 결과 계산. 즉 출력 z가 입력 x에 얼마나 민감한지 계산     
grad = tape.gradient(z, x)
# 연산결과를 Numpy 배열로 변환 후 출력
print("z:", z.numpy())
# 계산된 기울기(gradient)를 Numpy 배열로 변환 후 출력 
print("grad:", grad.numpy())




