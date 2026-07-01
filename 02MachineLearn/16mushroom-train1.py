import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split

# 데이터프레임 변환. header옵션으로 첫번째 행부터 데이터로 취급.  
mr = pd.read_csv("./resData/mushroom.csv", header=None)

# 데이터 내부의 기호를 숫자로 변환
label = []
data = []
# 데이터의 갯수만큼 반복 
for row_index, row in mr.iterrows():
    # 첫번째 컬럼은 레이블로 사용(독버섯 여부)
    label.append(row.loc[0])
    row_data = []
    # 두번째 컬럼부터는 버섯의 특성이므로 데이터로 사용 
    for v in row.loc[1:]:
        # 각 특성 문자를 아스키코드(정수)로 변환 후 리스트에 추가 
        row_data.append(ord(v))
    # 변환된 데이터를 data 리스트에 추가 
    data.append(row_data)
    # 전체 데이터중에서 첫번째 행(0번 인덱스)만 확인해보기 
    if row_index==0:
        print('row_data', row_data)
# 레이블 데이터 확인         
print('label', label)

# 학습 / 테스트 전용 데이터로 나누기 
data_train, data_test, label_train, label_test = \
    train_test_split(data, label)

# 데이터 학습시키기(랜덤 포레스트 사용)
clf = RandomForestClassifier()
clf.fit(data_train, label_train)

# 데이터 예측하기
predict = clf.predict(data_test)

# 결과 테스트하기
ac_score = metrics.accuracy_score(label_test, predict)
cl_report = metrics.classification_report(label_test, predict)
print("정답률 =", ac_score)
print("리포트 =\n", cl_report)

