# 모듈 임포트
import matplotlib.pyplot as plt
import pandas as pd
import json

# 알파벳 출현 빈도 데이터 읽기
with open("lang/freq.json", "r", encoding="utf-8") as fp:
    freq = json.load(fp)

# 언어마다 계산하기 : 각 언어별로 알파벳의 누적 횟수 계산 
lang_dic = {}
# 각 언어(lbl)마다 빈도 데이터(fq)를 꺼내온다. 
for i, lbl in enumerate(freq[0]["labels"]):
    fq = freq[0]["freqs"][i]
    if not (lbl in lang_dic):
        lang_dic[lbl] = fq
        continue
    # 빈도수를 딕셔너리로 저장 
    for idx, v in enumerate(fq):
        lang_dic[lbl][idx] = (lang_dic[lbl][idx] + v) / 2
# 콘솔에서 확인 
print('lang_dic', lang_dic)

# Pandas의 데이터프레임에 데이터 넣기
# char(97)~chr(122) 까지, 즉 'a'~'z'까지의 알파벳을 리스트로 생성 
asclist = [[chr(n) for n in range(97, 97+26)]]
# 리스트 컴프리헨션으로 생성한 리스트 확인 
print('asclist', asclist)
# 데이터프레임으로 변환 
df = pd.DataFrame(lang_dic, index=asclist)

# 그래프 그리기 
plt.style.use('ggplot')

# 막대그래프 : 그래프 생성 및 이미지 저장 
df.plot(kind="bar", subplots=True, ylim=(0, 0.15))
plt.savefig("./lang/lang-plot-bar.png")

# 선그래프 
df.plot(kind="line", subplots=True, ylim=(0, 0.15))
plt.savefig("./lang/lang-plot-line.png")

plt.show()