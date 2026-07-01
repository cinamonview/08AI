from sklearn import svm, metrics
import glob, os.path, re, json

# 텍스트를 읽어들이고 알파벳의 출현 빈도(frequency) 조사하기 
def check_freq(fname):
    # 매개변수로 전달된 파일경로를 통해 파일명 확인 
    name = os.path.basename(fname)
    ''' 
    파일명은 en-1.txt와 같은 형식을 가지고 있다. 
    정규표현식을 통해 파일명 앞부분의 단어를 얻어온다. 
      ^ : 문자열의 시작을 의미
      [a-z] : 소문자 a~z중 하나를 의미
      {2,} : 2개 이상 반복됨을 의미
    group() 함수는 매칭된 부분의 문자열을 반환한다. 즉 en, fr등의
    문자열이 lang에 저장된다. '''
    lang = re.match(r'^[a-z]{2,}', name).group()
    print('lang', lang)

    # 매개변수로 전달된 파일의 경로를 읽기 모드로 오픈 
    with open(fname, "r", encoding="utf-8") as f:
        text = f.read()
    # 텍스트 전체를 소문자로 변환 
    text = text.lower()
    # 알파벳은 모두 26글자이므로 이에 해당하는 리스트 생성
    #크기가 26이고, 모든 요소가 0으로 채워져있다. 
    cnt = [0 for n in range(0, 26)] # 리스트 컴프리핸션 문법 사용 
    code_a = ord("a") # 'a'의 아스키코드 값 : 97
    code_z = ord("z") # 'z'의 아스키코드 값
    # 텍스트 전체에서 알파벳 출현 횟수 구하기 
    for ch in text:
        # 각 문자의 아스키코드 구하기 
        n = ord(ch)
        # 출현하는 알파벳에 해당하는 인덱스의 값을 1 증가시킴 
        if code_a <= n <= code_z:
            # 즉 a가 출현했다면 0번 인덱스가 1 증가된다. 
            cnt[n - code_a] += 1
    # 출현 빈도 전체의 합을 계산 
    total = sum(cnt)
    # 알파벳의 등장횟수가 저장된 리스트의 데이터 정규화 
    freq = list(map(lambda n: n / total, cnt))
    # 빈도수와 언어(string)을 튜플로 반환 
    return (freq, lang)

# 각 파일 처리하기 
def load_files(path):
    # 빈도수와 레이블 저장을 위한 리스트 생성 
    freqs = []
    labels = []
    # "*.txt"와 같은 패턴을 이용해서 파일의 목록을 리스트로 생성 
    file_list = glob.glob(path)
    # 파일의 갯수만큼 반복 
    for fname in file_list:
        # 각 파일별로 빈도수 조사를 위한 함수 호출 
        r = check_freq(fname)
        # 반환되는 빈도수와 레이블을 각 리스트에 저장 
        freqs.append(r[0])
        labels.append(r[1])
    # 결과를 딕셔너리로 생성한 후 반환 
    return {"freqs":freqs, "labels":labels}

# 학습용, 테스트용 데이터 준비하기(파일의 패턴을 인수로 전달)
data = load_files("./lang/train/*.txt")
test = load_files("./lang/test/*.txt")

'''
[
    {
        'labels' : ['en', 'fr', 'id', 'tl'],
        'freqs' : [
            [0.xx, 0.yy, 0.zz, ...], #en의 알파벳 빈도
            [0.xx, 0.yy, 0.zz, ...], #fr의 알파벳 빈도 
            ...
        ]
freq.json 파일은 대략 위와 같은 형태를 가지고 있음 
'''
# 앞에서 확인된 언어별 빈도수 데이터를 json파일로 저장 
with open("lang/freq.json", "w", encoding="utf-8") as fp:
    json.dump([data, test], fp)

# 학습하기
clf = svm.SVC()
clf.fit(data["freqs"], data["labels"])

# 예측하기
predict = clf.predict(test["freqs"])

# 결과 테스트하기
ac_score = metrics.accuracy_score(test["labels"], predict)
cl_report = metrics.classification_report(test["labels"], predict)
print("정답률 =", ac_score)
print("리포트")
print(cl_report)

