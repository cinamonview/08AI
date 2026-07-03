


import cv2


# 숫자 인식을 위한 이미지 지정(하나씩 테스트)
# 아래 리스트는 ( 원본이미지명, 저장될 이미지명) 형태로 작성)
# TEST_IMG =['numbers.png','numbers_contour.png']
TEST_IMG =['numbers100.png','numbers100_contour.png']

# 이미지 로드
im = cv2.imread(f'./resData/{TEST_IMG[0]}')

# 그레이스케일로 변환
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

#가우시안 블러를 적용하여 노이즈를 제거
blur = cv2.GaussianBlur(gray,(5,5),0)

# 적응형 이진화 적용
thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
# 윤곽 추출하기
contours = cv2.findContours(thresh,
                            cv2.RETR_LIST,
                            cv2.CHAIN_APPROX_SIMPLE)[0]

# 추출한 윤곽을 반복 처리하기

for cnt in contours:
    # 윤곽을 감싸는 바운딩 바그 좌표 계산
    x,y,w,h = cv2.boundingRect(cnt)
    
    # 높이가 20미만이면 무시
    if h<20:
        continue
    red=(0,0,255)
    
    # 바운딩박스를 빨간색으로 표시
    cv2.rectangle(im,(x,y),(x+w,y+h),red,2)
    
# 윤곽선을 표시한 이미지 저장
cv2.imwrite(f'./saveFiles/{TEST_IMG[1]}',im)
print("Task Finished...!!!")