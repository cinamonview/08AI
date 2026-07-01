import urllib.request as req

# 데이터를 CSV로 다운로드
local= "./resData/mushroom.csv"
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data"
req.urlretrieve(url, local)
print("ok")


