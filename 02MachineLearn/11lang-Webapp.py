# 모듈 임포트 
from flask import Flask, request, render_template
import os
import joblib

# 플라스크 앱 실행을 위한 객체 생성 
app = Flask(__name__)

# 학습된 모델 로드(현재 경로 하위의 lang 폴더 지정함)
pklfile = os.path.dirname(__file__) + "/lang/freq.pkl"
clf = joblib.load(pklfile)

''' 
텍스트 입력 폼 및 판정 결과 출력을 위한 라우팅 설정 
페이지로 진입하는 부분과 폼값을 전송하는 2가지의 작업을 동시에 처리해야
하므로 get/post를 둘 다 지정한다. '''
@app.route('/', methods=['GET', 'POST'])
def index():
    # post방식으로 전송된 폼값을 받음 
    text = request.form.get('text', '')
    msg = ''
    # 입력받은 값이 있다면 함수를 호출해서 어떤 언어인지 판단 
    if text:
        lang = detect_lang(text)
        msg = "판정 결과: " + lang
    # 입력받은 값과 판정결과를 템플릿으로 전달
    return render_template('08lang-skin.html', 
                           text=text, msg=msg)

# 알파벳 출현 빈도로 언어 판별하기 
def detect_lang(text):
    # 사용자가 입력한 값을 소문자로 변경 
    text = text.lower()
    # a와 z의 아스키코드 얻기 
    code_a, code_z = (ord("a"), ord("z"))
    # 리스트 컴프리핸션으로 26개의 0으로 채워진 리스트 생성 
    cnt = [0 for i in range(26)]
    # 입력한 문자열의 길이만큼 반복
    for ch in text:
        # 해당 루프의 문자를 아스키코드를 구한 후 97을 차감한다. 
        #즉 a라면 0, b라면 1이 나옴. 
        n = ord(ch) - code_a
        # cnt 리스트의 특정 인덱스를 1증가 시킨다. 
        if 0 <= n < 26: cnt[n] += 1
    # 리스트에 저장된 정수의 총합 
    total = sum(cnt)
    if total == 0: return "입력이 없습니다"
    # 총합으로 각 요소를 나눠서 데이터 정규화 
    freq = list(map(lambda n: n / total, cnt))
    # 언어 예측 수행 
    res = clf.predict([freq])
    lang_dic = {"en": "영어", "fr": "프랑스어", "id": "인도네시아어",
                "tl": "타갈로그어"}
    # 결과 반환 
    return lang_dic.get(res[0], "알 수 없는 언어")

# 플라스크 시작 
if __name__ == "__main__":
    app.run(debug=True)



