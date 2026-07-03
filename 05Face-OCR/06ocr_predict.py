
import numpy as np
import cv2
from tensorflow.keras.models import load_model

# mnist학습 데이터 로드
mnist_model = load_model('./saveFiles/mnist_model.h5')

# 예측을 위한  이미지 로드
im = cv2.imread('resDAta/numbers100.PNG')
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
cv2.imwrite("./saveFiles/numbers100-binary.png",thresh)

#좌표 추출
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0]


#print("contours",contours)

# 좌표 정보를 저장할 리스트
rects=[]

#이미지의 가로 길이
im_w = im.shape[1]
#검출된 윤곽을 반복하며 숫자 후보 필터링

for i, cnt in enumerate(contours):
    #바운딩 박스 좌표 (x,y) 및 크기 (w,h) 계산
    x,y,w,h = cv2.boundingRect(cnt)
    if w< 10 or h<10:
        continue # skip 한다
    if w> im_w /5:
        continue # skip 한다
    y2= round(y/10) *10
    index = y2 * im_w +x
    rects.append((index,x,y,w,h))
    
# 정렬 수행
rects = sorted(rects, key=lambda x: x[0])

# 모델 입력 데이터를 저장할 리스트
X=[]

# 검출된 숫자 영역을 하나씩 처리
for i, r in enumerate(rects):
    index,x,y,w,h = r
    num = gray[y:y+h,x:x+w]
    num = 255-num
    ww = round((w if w>h else h) * 1.85)
    spc = np.zeros((ww,ww))
    wy = (ww-h) //2
    wx = (ww-w)//2
    spc [wy:wy+h, wx:wx+w] = num
    num = cv2.resize(spc,(28,28))
    
    # 확인용 이미지 저장
    
    if i <= 20:
        cv2.imwrite("./saveFiles/num-"+str(i)+"th.png",num)
        
    # 데이터 정규화 및 저장
    num = num.reshape(28*28)
    num = num.astype("float32") /255
    X.append(num)
    
#원주율을 숫자로 표현한 정답데이터를 리스트로 변환

s = "31415926535897932384" + \
    "62643383279502884197" + \
    "16939937510582097494" + \
    "45923078164062862089" + \
    "98628034825342117067"

answer=list(s) 
ok = 0


# 예측
nlist = mnist_model.predict(np.array(X))

# 정답확인
for i,n in enumerate(nlist):
    ans = n.argmax()
    if ans == int(answer[i]): # 정답인경우
        ok += 1
    else: #오답인경우
        print("[ng]",i,"번째",ans,"!=",answer[i],np.int32(n*100))
print("정답률 : ",ok /len(nlist))