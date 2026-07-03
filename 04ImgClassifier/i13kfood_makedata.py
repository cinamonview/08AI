import numpy as np
import cv2
import glob
import os
from sklearn.model_selection import train_test_split

# 학습할 이미지가 저장된 폴더 및 카테고리 설정 
root_dir = "./kfood"
categories = ["FriedChicken", "Kimchi", "MiyeokGuk", "Ramen", "Samgyeopsal"]
# 학습용 이미지를 정사각형으로 만들기 위해 사이즈 지정
image_size = 224

# 이미지 데이터
X = []
# 레이블 데이터 
Y = []

# 이미지 로드 및 리사이징 함수 
def load_and_resize_image(path):
    # OpenCV 모듈을 이용해서 이미지를 읽음 
    img = cv2.imread(path)
    # 이미지 경로가 잘못되었거나 이미지가 아니라면 즉시 종료 
    if img is None:
        print(f"[읽기 실패] {path}")
        return None
    # RGB 변환 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 이미지의 가로, 세로 크기 
    h, w, _ = img.shape
    # 가로와 세로 길이 중 긴쪽에 맞춰서 이미지 길이 계산 
    if h > w:
        new_h, new_w = image_size, int(w * (image_size / h))
    else:
        new_h, new_w = int(h * (image_size / w)), image_size
    # 계산된 가로, 세로 길이를 통해 리사이징 처리 
    img = cv2.resize(img, (new_w, new_h))
    # 정사각형으로 만들기 위해 패딩 추가 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pad_h = (image_size - new_h) // 2
    pad_w = (image_size - new_w) // 2
    img = cv2.copyMakeBorder(img, pad_h, image_size - new_h - pad_h,
                             pad_w, image_size - new_w - pad_w,
                             cv2.BORDER_CONSTANT, value=[0, 0, 0])
    return img

# 음식 카테고리의 리스트를 통해 반복 
all_data = []
# 5개의 음식 폴더를 반복 
for idx, category in enumerate(categories):
    # 루트폴더와 카테고리명을 병합해서 이미지의 경로 생성
    image_dir = os.path.join(root_dir, category)
    # 해당 경로의 모든 파일을 리스트로 반환 
    files = glob.glob(image_dir + "/*")
    # 이미지 처리 중 확인용 로그 출력 
    print(f"{category} 처리 중... ({len(files)}개)")
    # 폴더 내 모든 이미지를 대상으로 리사이징 반복 처리 
    for file in files:
        img = load_and_resize_image(file)
        if img is not None:
            # (이미지데이터, 레이블)
            # categories 리스트의 인덱스가 레이블로 입력됨(치킨이면 0)
            all_data.append((img, idx))

# 데이터 셔플 
np.random.shuffle(all_data)

# 데이터분리. 리스트로 만든 후 numpy배열로 변환한다. 
X_data = np.array([x[0] for x in all_data])
Y_data = np.array([x[1] for x in all_data])
# 훈련용 / 테스트용 데이터로 분리. test_size 옵션이 있으므로 80:20 적용. 
X_train, X_test, Y_train, Y_test = (
    train_test_split(X_data, Y_data, test_size=0.2, random_state=42))

# npz 파일로 저장 
np.savez(root_dir+"/kfood_dataset.npz", X_train=X_train, X_test=X_test,
         Y_train=Y_train, Y_test=Y_test)
print("Task Finished..!!")




