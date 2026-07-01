# 판다스 모듈 임포트 
import pandas as pd
from sklearn import svm, metrics

# XOR 논리 데이터 
xor_input = [
    [0, 0, 0],
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]

#데이터를 데이터프레임으로 변환 
xor_df = pd.DataFrame(xor_input)
# 학습 전용 데이터와 테스트(레이블) 전용 데이터로 분류 
xor_data = xor_df.loc[:, 0:1] #데이터
xor_label = xor_df.loc[:, 2] #레이블
print('xor_data\n', xor_data)

# 데이터 학습 및 예측 
clf = svm.SVC()
clf.fit(xor_data, xor_label)
pre = clf.predict(xor_data)

# 정답률 구하기 
ac_score = metrics.accuracy_score(xor_label, pre)
print("정답률 =", ac_score)
''' 싸이킷런에서 제공하는 내장함수를 통해 학습용 프로그램을 간단히
작성할 수 있다. '''