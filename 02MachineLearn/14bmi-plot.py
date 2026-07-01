import matplotlib.pyplot as plt
import pandas as pd

# CSV파일을 데이터프레임으로 변환. 세번째 열을 행 인덱스로 지정함.  
tbl = pd.read_csv("./resData/bmi.csv", index_col=2)
print('tbl', tbl)

# 그래프 및 Axe 객체 생성 
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# 산점도 생성을 위한 함수(지정한 레이블을 임의의 색깔로 표현)
def scatter(lbl, color):
    b = tbl.loc[lbl]
    # x축은 몸무게, y축은 키로 설정 후 산점도 생성
    ax.scatter(b["weight"], b["height"], c=color, label=lbl)

# 비만, 정상, 저체중 순으로 산점도 그리기 
scatter("fat", "red")
scatter("normal", "yellow")
scatter("thin", "purple")

# 범례 표시, 그래프를 이미지로 저장 
ax.legend()
plt.savefig("./saveFiles/bmi-scatter.png")
plt.show()

