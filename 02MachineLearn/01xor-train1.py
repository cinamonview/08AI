
# 사이킷런의 SVM모듈 임포트
from sklearn import svm

'''
XOR의 논리 결과 데이터 :
    배타적 논리합인 XOR는 두 입력값이 동일하면 FALSE
    다르면 TRUE를 반환한다.
    이 4가지의 논리를 데이터로 정의한다.
    1,2 열은 학습데이터, 3열은 정답(레이블) 데이터로 사용한다.'''


# XOR 의 계산 결과 데이터

xor_data = [
    [0,0,0],
    [0,1,1],
    [1,0,1],
    [1,1,0],
]

# 학습을 위해 학습용과 레이블용 데이터로 분리하기 위해서 리스트를 생성한다.

# 학습을 위해 데이터와 레이블 분리하기

data=[]  # 학습용 데이터 저장용
label = []  # 레이블 데이터 저장용
# 데이터 수만큼 반복한다.
for row in xor_data:
    # 앞의 두개는 학습데이터로 사용
    p=row[0]
    q=row[1]
    # 마지막은 레이블 데이터로 사용
    r=row[2]
    # 각 리스트에 데이터 추가
    data.append([p,q])
    label.append(r)
    
# 분류기 (Classifier) 객체 생성
'''
분류기(Classifier) 객체 생성 
svc(Support Vector Classification)
    서포트 벡터 머신 분류 모델을 생성하는 클래스로,
    분류 작업에 적합한 SVM 모델 객체를 사용한다.
    이 객체를 통해 데이터를 학습(fit)하고
    예측 (predict)을 수행할 수 있다.
'''

clf = svm.SVC()

# 데이터 학습시키기 (데이터와 레이블을 인수로 전달한다.)

clf.fit(data,label)

# 데이터 예측하기 : 예측하고 싶은 데이터를 전달하면
    # 데이터 수만큼 예측 결과를 반환해 준다. 
pre = clf.predict(data)
print(" 예측결과 : ",pre)

# 결과 확인하기 :

ok = 0; total = 0
# 레이블 데이터를 통해 반복해서 index와 data를 동시에 인출
for idx , answer in enumerate(label):
    # 예측 결과 데이터와 하나씩 비교
    p=pre[idx]
    if p == answer:
        ok += 1  # 예측이 맞는 경우 1 증가
    total += 1  # 각 데이터마다 1 증가 ( 데이터의 갯수 )
    
# 데이터가 4개 밖에 안되므로 100%의 결과가 나온다.
print(" 정답률 : ", ok, "/" , total , "=" , ok/total)