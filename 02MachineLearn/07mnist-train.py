from sklearn import model_selection, svm, metrics

# csv 파일을 읽어들이고 가공하기 
def load_csv(fname):
    # 레이블과 이미지 데이터를 저장할 리스트 
    labels = []
    images = []
    # 매개변수로 전달받은 csv파일의 경로를 이용해서 '읽기'모드로 파일오픈
    with open(fname, "r") as f:
        # 파일의 내용을 한줄씩 읽은 후 ... 
        for line in f:
            # 콤마로 구분되어 있으므로 split해서 배열로 반환 
            cols = line.split(",")
            # split한 배열의 크기가 2미만이면 정상 데이터가 아니므로 통과
            if len(cols) < 2: continue
            # 0번 인덱스는 레이블(정답)이므로 삭제 후 반환되는 값을 label
            #리스트에 추가한다. 
            labels.append(int(cols.pop(0)))
            # 정답을 제외한 나머지 부분은 픽셀데이터 이므로 정규화를 위해
            #256으로 나눠서 0~1사이의 값으로 만든다. 
            vals = list(map(lambda n: int(n) / 256, cols))
            # images 리스트에 추가 
            images.append(vals)
    return {"labels":labels, "images":images}

# csv파일을 정규화된 데이터로 변환 
data = load_csv("./resMnist/train.csv")
test = load_csv("./resMnist/t10k.csv")

# 학습하기 
clf = svm.SVC()
clf.fit(data["images"], data["labels"])

# 예측하기
predict = clf.predict(test["images"])

# 결과확인 
ac_score = metrics.accuracy_score(test["labels"], predict)
# 리포트 출력하기 
cl_report = metrics.classification_report(test["labels"], predict)
print("정답률 =", ac_score)
print("리포트 =")
print(cl_report)

