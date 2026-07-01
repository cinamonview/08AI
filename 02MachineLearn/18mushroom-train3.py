import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split

# 데이터 읽어 들이기
mr = pd.read_csv("./resData/mushroom.csv", header=None)

# 레이블(정답)과 특징 데이터 분리
# 0번 컬럼은 독성 여부(label), 1번부터 끝까지는 특징(data)
label = mr.iloc[:, 0]
features = mr.iloc[:, 1:]

# 원-핫 인코딩 적용 (핵심 부분)
# 모든 문자열(범주형) 컬럼을 자동으로 0과 1의 컬럼들로 전개합니다.
data = pd.get_dummies(features)

# 변환된 데이터의 형태 확인 (컬럼 수가 자동으로 결정됨)
print("원-핫 인코딩 후 데이터 형태:", data.shape)

# 학습 전용 데이터와 테스트 전용 데이터로 나누기
data_train, data_test, label_train, label_test = \
train_test_split(data, label)

# 데이터 학습시키기
clf = RandomForestClassifier()
clf.fit(data_train, label_train)

# 데이터 예측하기
predict = clf.predict(data_test)

# 결과 테스트하기
ac_score = metrics.accuracy_score(label_test, predict)
print("정답률 =", ac_score)



