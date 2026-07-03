import cv2

# 입력 파일 지정
# image_file = "./resData/photo1.jpg"
image_file = "./resData/photo2.jpg"

# 캐스케이드 파일의 경로 지정
cascade_file = cv2.data.haarcascades + "haarcascade_frontalface_alt.xml"
'''
이 XML 파일은 사전에 학습된 데이터를 기반으로 얼굴을 감지한다.
해당 경로에 들어가보면 얼굴뿐 아니라 눈,코,입 등을 
감지하는 파일도 있다.
'''

print('cascade_file', cascade_file)


# 이미지 읽기 numpy 배열의 형태로 이미지 데이터를 저장.

image = cv2.imread(image_file)

# 그레이 스케일로 변환
image_gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 얼굴 인식을 위한 특징 파일 로드
cascade = cv2.CascadeClassifier(cascade_file)

# 얼굴 인식 실행

face_list = cascade.detectMultiScale(image_gs,
                                     scaleFactor=1.1,
                                     minNeighbors = 1,
                                     minSize=(150,150))
'''
scaleFactor :
    이미지 크기를 10%씩 축소하면서 여러 크기의 얼굴을 감지.
    1.1 보다 크면 더 적은 얼굴을 감지하고,
    그보다 작으면 더 많은 얼굴을 감지하지만 오탐 가능성이 증가된다.
minNeighbors : 
    얼굴 후보가 검출될때 주변의 이웃 후보 갯수를 설정.
    값이 클수록 더 엄격한 기준으로 얼굴을 판단함
minSize :
    검출할 최소 얼굴 크기 지정. 가로 세로 150px보다 작은 얼굴은
    무시한다.
'''

# 얼굴이 인식 되었다면..
if len (face_list) > 0:
    # 인식한 부분의 좌표 출력
    print(face_list)
    color = (0,0,255) #빨강색 설정 ( OPEN CV 에서는 BGR 순으로 지정한다.)
    
    #얼굴 영역에 빨간 테두리 표시
    for face in face_list:
        x,y,w,h = face
        '''
        x,y : 얼굴의 좌상단 좌표값
        w,h : 가로(폭), 세로(높이) 길이
        thickness : 선의 두께
        '''
        
        # 얼굴 위치에 사각형 테두리 표시
        cv2.rectangle(image,(x,y),(x+w,y+h),color,thickness = 8)
        
        # 파일로 출력
        # cv2.imwrite("./saveFiles/photo1-facedetect01.png",image)
        cv2.imwrite("./saveFiles/photo1-facedetect02.png",image)
else:
    print("얼굴을 인식할 수 없습니다")