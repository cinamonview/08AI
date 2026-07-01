from sklearn import svm, metrics
import random, re

# 붓꽃의 csv 데이터 읽어들이기
# 데이터 저장을 위한 리스트 생성 
csv = []
# csv 파일을 읽기(r)모드로 오픈 
with (open('resData/iris.csv', 'r', encoding='utf-8') as fp):
    # 파일의 내용을 한줄씩 읽기 
    for line in fp:
        # 줄바꿈 제거 
        line = line.strip()
        # 컴마를 기준으로 문자열을 분리해서 배열로 반환 
        cols = line.split(',')
        ''' 
        문자열 데이터를 실수로 변환하는 기능으로 람다식 정의 
        csv파일에서 읽어온 데이터는 문자이므로 실수로 변환이 필요하다. 
        정규표현식을 통해 정의함
            ^ : 문자열의 시작
            [0-9\.] : 숫자(0~9) 또는 마침표(.)가 한번이상 나타나는
                패턴을 의미
            $ : 문자열의 끝
            따라서 123 혹은 12.34와 같은 문자와 매칭된다. 
        '''
        # 정규표현식과 매칭되면 float()를 통해 실수로 변환 
        #즉 훈련데이터는 실수로, 레이블데이터는 문자 그대로 사용한다. 
        fn = lambda n : float(n) if re.match(r'^[0-9\.]+$', n) \
            else n
        # cols의 크기만큼 반복해서 fn을 호출한 결과로 리스트를 생성 
        cols = list(map(fn, cols))
        # 이렇게 만들어진 결과를 csv 리스트에 추가한다. 
        csv.append(cols)
# 첫번째 줄의 헤더는 제거한다.(컬럼명이 입력되어 있음)        
del csv[0]
# 데이터 셔플. 즉 전체적으로 섞어준다. 
random.shuffle(csv)
# 전체 데이터의 갯수 확인 
total_len = len(csv)
print("데이터갯수", total_len)

# 학습데이터 100개와 테스트데이터 50개로 분할하기 
''' 
데이터를 이와같이 나누는 이유는 훈련에 사용하지 않은 데이터를 테스트에
활용해야 학습이 제대로 되었는지 확인할 수 있기 때문이다. '''
train_len = int(total_len * 2 / 3) 
# 훈련용 학습데이터 / 레이블데이터를 저장하기 위한 리스트 
train_data = []
train_label = []
# 테스트용 학습데이터 / 레이블데이터 
test_data = []
test_label = []
# 전체 데이터 갯수만큼 반복 
for i in range(total_len):
    # 학습 및 레이블 데이터로 분리 
    data  = csv[i][0:4] # 0~3열까지
    label = csv[i][4] # 4열 
    if i < train_len:
        # 훈련용 데이터 추가 : 100개 
        train_data.append(data)
        train_label.append(label)
    else:
        # 테스트 데이터 추가 : 50개 
        test_data.append(data)
        test_label.append(label)

# 데이터를 학습시키고 예측하기 
clf = svm.SVC()
clf.fit(train_data, train_label)
pre = clf.predict(test_data)

# 정답률 구하기 
ac_score = metrics.accuracy_score(test_label, pre)
print("정답률 =", ac_score)


