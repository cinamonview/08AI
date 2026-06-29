


import urllib.request as req
import gzip, os, os.path

# 파일 다운로드 시 진행률을 콘솔에 표시

def progress(block_num, block_size, total_size):
   downloaded = block_num * block_size
   percent = (downloaded / total_size) * 100 if total_size > 0 else 0
   print(f"다운로드 진행률: {percent:.2f}%")

# 파일을 저장할 디렉토리 지정
savepath = "./resMnist"
# 다운로드 URL 지정
baseurl = "https://github.com/golbin/TensorFlow-MNIST/raw/master/mnist/data/"
# 실제 다운로드할 파일명을 리스트로 정리해보았다.
files = [
    "train-images-idx3-ubyte.gz",
    "train-labels-idx1-ubyte.gz",
    "t10k-images-idx3-ubyte.gz",
    "t10k-labels-idx1-ubyte.gz"]


# 디렉토리가 없으면 자동으로 생성해준다.

if not os.path.exists(savepath) : os.mkdir(savepath)

#배열로 선언한 각 파일을 다운로드
# 리스트로 선언한 각 파일의 갯수만큼 반복하면서 다운로드
for f in files:
    # 다운로드 및 저장 경로 조립
    url = baseurl +"/" + f  # 깃헙주소
    loc = savepath + "/" + f # 세이브패쓰의 주소
    print("download : ", url)
    # 조립한 경로에 파일이 있다면..
    if not os.path.exists(loc):
        # 다운로드 진행. URL로부터 다운로드 후 loc에 저장한다.
        req.urlretrieve(url, loc)
        # 진행률을 보면서 확인하고 싶다면 3번째 인수로 함수명 추가해준다.
        # req.urlretrieve(url, loc, progress) 
        
        
# GZip 파일 압축 해제

for f in files:
    # 원본 파일과 압축해제된 Raw파일의 경로 설정
    gz_file = savepath + "/" +f
    raw_file = savepath + "/" + f.replace(".gz","")
    print("gzip : ", f)
    # 파일을 열어서 읽은 후 쓰기. 즉 압축해제를 해준다.
    # rb = read wb = write
    with gzip.open(gz_file,"rb") as fp:
        body = fp.read()
        with open(raw_file,"wb") as w:
            w.write(body)
            
            
# 실행 종료
print("ok")

# raw파일들 이기때문에 읽어서 csv 파일로 만드는 과정이 필요하다!