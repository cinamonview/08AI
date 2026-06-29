import os
import glob
from PIL import Image
import matplotlib.pyplot as plt

# PGM 파일들이 저장된 디렉토리 경로
directory_path = 'resMnist'

# 패턴에 맞는 모든 파일 찾기
file_pattern = os.path.join(directory_path, 't10k-*-*.pgm')
pgm_files = glob.glob(file_pattern)
print(pgm_files)

# 각 파일에 대해 한 장씩 이미지 출력
for pgm_file in pgm_files:
    img = Image.open(pgm_file)

    # 이미지를 출력
    plt.imshow(img, cmap='gray')
    plt.title(f"Image: {pgm_file}")  # 파일명 제목으로 표시
    plt.axis('off')  # 축 숨기기
    plt.show()  # 한 장씩 표시

