import urllib.request as req
import gzip, os, os.path

# 파일 다운로드시 진행률을 콘솔에 표시 
# def progress(block_num, block_size, total_size):
#     downloaded = block_num * block_size
#     percent = (downloaded / total_size) * 100 if total_size > 0 else 0
#     print(f"다운로드 진행률: {percent:.2f}%")

# 파일을 저장할 디렉토리 지정 
savepath = "./resMnist"
# 다운로드 URL 지정 
baseurl = "https://github.com/golbin/TensorFlow-MNIST/raw/master/mnist/data/"
# 다운로드 할 파일명을 리스트로 정리 
files = [
    "train-images-idx3-ubyte.gz",
    "train-labels-idx1-ubyte.gz",
    "t10k-images-idx3-ubyte.gz",
    "t10k-labels-idx1-ubyte.gz"]

# 디렉토리가 없으면 자동으로 생성 
if not os.path.exists(savepath):
    os.mkdir(savepath)

# 리스트로 선언한 각 파일의 갯수만큼 반복하면서 다운로드 
for f in files:
    # 다운로드 및 저장 경로 조립 
    url = baseurl + "/" + f
    loc = savepath + "/" + f
    print("download:", url)
    # 조립한 경로에 파일이 있다면..
    if not os.path.exists(loc):
        # 다운로드 진행. url로부터 다운로드 후 loc에 저장 
        req.urlretrieve(url, loc)
        # 진행률을 보고싶다면 3번째 인수로 함수명 추가 
        # req.urlretrieve(url, loc, progress)

# GZip 파일 압축 해제 
for f in files:
    # 원본파일과 압축해제된 Raw파일의 경로 설정 
    gz_file = savepath + "/" + f
    raw_file = savepath + "/" + f.replace(".gz", "")
    print("gzip:", f)
    # 파일을 열어서 읽은 후 쓰기. 즉 압축해제한다. 
    with gzip.open(gz_file, "rb") as fp:
        body = fp.read()
        with open(raw_file, "wb") as w:
            w.write(body)

print("ok")