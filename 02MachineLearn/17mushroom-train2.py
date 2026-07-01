import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split

# 데이터 읽어 들이기
mr = pd.read_csv("./resData/mushroom.csv", header=None)

# 데이터 내부의 분류 변수 저장용 리스트
label = []
data = []
attr_list = []

# 원-핫 인코딩 적용
# 데이터프레임의 행(row)을 하나씩 반복하며 처리
for row_index, row in mr.iterrows():
    # 첫번째 열은 독성여부이므로 label에 추가 
    label.append(row.loc[0])
    # 레이블을 제외한 버섯의 특징 데이터를 담을 임시 리스트 
    exdata = []
    # 두번째 열부터 마지막까지 반복하면서 특징 데이터 처리 
    for col, v in enumerate(row.loc[1:]):
        # 첫번째 행일때는 특징을 위한 딕셔너리 생성 
        if row_index == 0:
            attr = {"dic": {}, "cnt":0}
            attr_list.append(attr)
        else:
            # 두번째 행부터는 이미 생성된 딕셔너리 사용 
            attr = attr_list[col]

        # 원-핫 인코딩을 위해 12개의 0으로 채워진 리스트 생성 
        d = [0,0,0,0,0,0,0,0,0,0,0,0]
        # 현재 읽은 특징기호(v)가 이미 딕셔너리에 등록되어 있다면 그 
        #번호(idx)를 가져온다. 
        if v in attr["dic"]:
            idx = attr["dic"][v]
            # print('true', idx)
        # 처음 등장하는 기호라면 새로 등록하고 번호를 부여한다. 
        else:        
            idx = attr["cnt"]
            attr["dic"][v] = idx
            attr["cnt"] += 1
            # print('false', idx)
        # 해당 기호에 부여된 번호(idx) 위치의 값을 1로 바꿔준다. 
        d[idx] = 1
        # 원-핫 인코딩 된 결과 확인하기(버섯의 모양일때만 데이터 확인)
        if col == 0:
            print(v, d)
        # 변환된 [1,0,0..] 리스트를 전체 데이터 행에 누적해서 연결 
        exdata += d
    # 학습용 리스트에 추가 
    data.append(exdata)

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






