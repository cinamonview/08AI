


from PIL import Image
import os,glob
import numpy as np
from sklearn.model_selection import train_test_split

# 분류 대상 카테고리 5개 선택 및 경로 설정
caltech_dir = "./caltech101/101_ObjectCategories"
# 의자 ~ 플라밍고 까지 선택해서 리스트로 정의
categories = ["chair","camera","butterfly","elephant","flamingo"]
# 클래스의 크기 5
nb_classes = len(categories)


# 이미지 리사이즈 크기 지정
image_w = 64
image_h = 64

# RGB이므로 3채널( RED GREEN BLUE)의 픽셀 수 계산
pixels = image_w*image_h *3

# 이미지 데이터와 레이블(정답) 을 저장할 리스트
X=[]
Y=[]

# 5개의 카퉤고리 반복 실행

for idx, cat in enumerate(categories) :
    # 레이블은 우선 모든 클래스에 대해 0으로 설정
    label = [0 for i in range(nb_classes)]
    '''
    현재 카테고리의 인덱스에 해당하는 클래스 요소를 1로 변경
    즉, 원-핫 인코딩 형식으로 레이블을 생성한다.
    '''
    
    # 현재 카테고리의 인덱스에 해당하는 클래스에 대해 1을 설정
    label[idx] =1
    # 이미지 폴더의 경로 설정
    image_dir = caltech_dir+"/"+cat
    # glob() 함수를 사용하여
    # 폴더내의 모든 jpg 이미지 파일을  가져오기
    files = glob.glob(image_dir+"/*.jpg")
    # 이미지의 갯수만큼 반복
    
    for i , f in enumerate(files):
        # 이미지 오픈 후 RGB 모드 변환 및 리사이즈 크기 조정 (64*64)
        img = Image.open(f)
        img = img.convert("RGB")
        img = img.resize((image_w,image_h))
        
        # 이미지를 numpy 배열로 변환
        data = np.asarray(img)
        # 이미지와 레이블데이터를 리스트에 추가
        X.append(data)
        Y.append(label)
        # 변환된 데이터를 콘솔에 출력해서 확인( 10개마다 )
        if i % 10 ==0:
            print(i, "\n" , data)
            
# 리스트를 ndarray로 변환
X= np.array(X)
Y= np.array(Y)

# 학습 전용 데이터와 테스트 전용 데이터 구분
# 훈련용 /테스트용 데이터로 분리
X_train, X_test, Y_train, Y_test = train_test_split(X,Y)
print(X_train.shape,X_test.shape,Y_train.shape, Y_test.shape)

# NPZ 포맷으로 저장
np.savez("./saveFiles/caltech_5object.npz", X_train = X_train,X_test = X_test,Y_train=Y_train,Y_test=Y_test)

'''
즉 학습에 사용할 이미지를 적당한 크기로 리사이즈 한 후
numpy 배열 형식으로 변환하고 데이터셋으로 저장한다.
MNIST 데이터셋이 이와 같은 방식으로 만들어진거라 볼 수 있다.
'''

print("Task Finished...!!!",len(Y)) 
    