
from PIL import Image
import numpy as np
import os,re

# 파일 경로 지정
# 이미지가 저장된 경로 설정
search_dir = "./caltech101/101_ObjectCategories"
# Average Hash 값을 저장한 캐시파일을 저장할 경로 설정
cache_dir = "./caltech101/cache_avhash"
# 캐시 디렉토리가 없으면 생성하기 
if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)
    
# 이미지 데이터를 Average HAsh로 변환

def average_hash(fname, size =16):
    fname2 = fname[len(search_dir):]
    # 경로의 구분자 변경
    fname2 = fname2.replace("\\","/")
    # 캐시파일의 경로 생성( 파일명의 경로를 통해 생성함 CSV로!)
    cache_file = cache_dir + "/" + fname2.replace('/','_')+".csv"
    
    
    # 캐시 파일이 없을 경우 AVerage HAsh 생성
    if not os.path.exists(cache_file):
        # 파일 오픈 후 그레이 스케일로 변경, 리사이즈 등 작업 진행!
        img = Image.open(fname)
        img = img.convert('L').resize((size,size), Image.Resampling.LANCZOS)
        pixels = np.array(img.getdata()).reshape((size,size))
        avg = pixels.mean()
        px = 1* (pixels > avg)
        # Average Hash로 변환된 데이터를 csv 파일로 저장!
        np.savetxt(cache_file,px,fmt="%.0f", delimiter =",")
    else:
        # 캐시 파일이 존재하면 데이터를 읽어 numpy 배열로 로드~!
        px = np.loadtxt(cache_file,delimiter=",")
        
    return px


# 해밍 거리 계산

def hamming_dist(a,b):
    # 2개의 해시값을 받은 후 2차원 배열로 변환~
    aa = a.reshape(1,-1)
    ab = b.reshape(1,-1)
    # 서로 다른 원소의 갯수를 합산하여 해밍거리 계산.
    dist = (aa != ab).sum()
    return dist


# 주어진 디렉토리 경로에서 하위 디렉토리를 포함한 모든 파일을 순회

def enum_all_files(path):
    for root,dirs,files in os.walk(path):
        for f in files:
            # 파일명을 얻어온 후 
            fname = os.path.join(root,f)
            # 해당 확장자만 파일명 반환
            if re.search(r'\.(jpg|jpeg|png)$',fname):
                yield fname
                
                
# 이미지 찾기

def find_image(fname,rate):
    src = average_hash(fname)
    # 검색 대상의 데렉토리의 모든 파일을 비교
    for fname in enum_all_files(search_dir):
        fname2 = fname.replace("\\","/")
        dst = average_hash(fname)
        # 두 이미지간의 해밍거리 계산후 256으로 나눠서 이미지간의 유사도를 계산
        diff_r = hamming_dist(src,dst) / 256
        # 유사도가 기준(rate) 이하인 경우만 결과를 반환!
        if diff_r <rate:
            yield (diff_r, fname)

            
# 검색할 기준 이미지 경로 설정
# srcfile = search_dir + "/chair/image_0016.jpg"
srcfile = search_dir + "/brain/image_0016.jpg"
html = ""
# 유사한 이미지 검색 ( rate: 0.25 )
sim = list(find_image(srcfile, 0.25))
sim = sorted(sim, key=lambda x:x[0])
for r, f in sim:
    print(r, ">", f)
    # 검색된 이미지의 갯수만큼 HTML 태그로 추가 ( img 태그 사용 )
    f2 = "." + f
    s = '<div style="float:left;"><h3>[ 차이 :' + str(r) + '-' + \
        os.path.basename(f) + ']</h3>'+ \
        '<p><a href="' + f2 + '"><img src="' + f2 + '">'+ \
        '</a></p></div>'
    html += s

# HTML로 출력하기
html = """<html><head><meta charset="utf8"></head>
<body><h3>원래 이미지</h3><p>
<img src='{0}'></p>{1}
</body></html>""".format("."+srcfile, html)
with open("./saveFiles/avhash-search-output.html2", "w", encoding="utf-8") as f:
    f.write(html)
print("HTML 저장 Ok")

