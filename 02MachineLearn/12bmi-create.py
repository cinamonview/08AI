# 난수 생성을 위한 모듈 
import random

# BMI 지수를 계산해서 레이블을 반환하는 함수 
def calc_bmi(h, w):
    # BMI 지수를 구하는 공식 적용 
    bmi = w / (h/100) ** 2
    # 계산된 지수에 따른 레이블 반환 
    if bmi < 18.5: return "thin"
    if bmi < 25: return "normal"
    return "fat"

# 파일을 w(쓰기) 모드로 열었으므로 없으면 생성된다. 
fp = open("./resData/bmi.csv", "w", encoding="utf-8")
# 첫번째 줄에는 컬럼명 추가 
fp.write("height,weight,label\r\n")

# 카운트를 위한 딕셔너리 생성 
cnt = {"thin":0, "normal":0, "fat":0}
# 2만개의 데이터 생성 
for i in range(20000):
    # 키 생성
    h = random.randint(120,200)
    # 몸무게 생성
    w = random.randint(35, 80)
    # 생성된 키와 몸무게를 통해 BMI 계산 
    label = calc_bmi(h, w)
    # 3가지의 Key중 하나를 1 증가 
    cnt[label] += 1
    # csv 파일에 키, 몸무게, BMI지수를 한행씩 추가 
    fp.write("{0},{1},{2}\r\n".format(h, w, label))
fp.close()
print("ok,", cnt)

