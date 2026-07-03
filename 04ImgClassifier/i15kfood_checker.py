# 기존 14번 예제파일을 모듈로 임포트 후 kfood로 별칭 부여

import i14kfood_CNN as kfood
import sys,os
from PIL import Image
import cv2   # OpenCV 모듈
import numpy as np
from datetime import datetime

# 명령줄에서 파일 이름 지정

'''
실행 방법 : 
    CMD (명령프롬프트)에서 현재 파일이 있는 위치로 이동한 후
    디렉토리> python i15kfood_checker.py 음식이미지1 음식이미지2..부터 음식이미지n까지
'''

# 프로그램 실행시 예측을 위한 이미지경로(파라미터)가 없으면 실행종료
if len(sys.argv) <=1:  
    print("소스파일.py (<파일이름>)")
    quit()

# 이미지의 리사이즈 크기 및 카테고리 지정
image_size = 224
categories = ["프라이드 치킨", "김치","미역국","라면","삼겹살"]
calories = [100,200,300,400,500]

# 입력 이미지를 Numpy로 변환
X=[]
files = []

# 예측을 위해 전달한 이미지의 갯수만큼 반복
for fname in sys.argv[1:]:
    # 이미지 읽기 
    img = cv2.imread(fname)
    if img is None:
        continue
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # RGB변환
    h,w,_ = img.shape
    if h>w:
        new_h, new_w = image_size,int(w*(image_size/h))
    else:
        new_h,new_w = int(h*(image_size/w)), image_size
    img = cv2.resize(img,(new_w,new_h))
    
    #정사각형으로 패딩 추가
    
    pad_h = (image_size - new_h)//2
    pad_w = (image_size - new_w)//2
        
        
    img = cv2.copyMakeBorder(img,pad_h,image_size-new_h-pad_h,pad_w,image_size-new_w-pad_w,cv2.BORDER_CONSTANT,value=[0,0,0])
    
    # 리스트에 추가
    X.append(img)
    files.append(fname)
    
# 예측을 위한 이미지를 정사각형 형태로 만든 후 넘파이 배열로 변환
X= np.array(X)


# CNN  모델 구축 (i 14번 예제의 함수 호출 (build_model))
model = kfood.build_model(X.shape[1:])
# 기존 생성한 가중치 모델을 메모리에 로드.
model.load_weights("./kfood/kfood_model.weights.h5")

# 데이터 예측
html = ""
pre = model.predict(X)
for i, p in enumerate(pre):
   y = p.argmax()
   # 예측을 위한 이미지 정보를 콘솔에서 확인.
   print("+입력:", files[i])
   print("|음식이름:", categories[y])
   print("|칼로리:", calories[y])
   html += """
       <h3>입력:{0}</h3>
       <div>
         <p><img src="..\{1}" width=300></p>
         <p>음식이름:{2}</p>
         <p>칼로리:{3}kcal</p>
       </div>
   """.format(os.path.basename(files[i]),
       files[i],
       categories[y],
       calories[y])


# 리포트를 HTML로 저장
# 저장을 위해 HTML 태그로 작성
html = "<html><body style='text-align:center;'>" + \
   "<style> p { margin:0; padding:0; } </style>" + \
   html + "</body></html>"

# 저장시에는 현재 날짜 및 시간을 이용해서 파일명 생성
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open("./kfood/kfood_result_"+timestamp+".html", "w") as f:
   f.write(html)


print("Task Finished..!!")
