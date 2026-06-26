

import numpy as np


# 1~9까지 배열 생성
array1 = np.arange(start=1, stop=10)
# 0~2까지 슬라이싱
array2 = array1[0:3]
print('array2', array2)
# 타입은 ndarray로 출력됨
print('타입1', type(array1))
print('타입2', type(array2))

# 처음부터 2까지 슬라이싱
array3 = array1[:3]
print('array3', array3)

# 3부터 끝가지 슬라이싱
array4 = array1[3:]
print('array4', array4)

# 배열 전체 선택
array5 = array1[:]
print('array5',array5)

###########################################################################################



# 3행 3열인 2차원 배열
array1d = np.arange(start=1,stop=10)
array2d = array1d.reshape(3,3)
print('array2d:\n',array2d)

# 2차원 배열의 슬라이싱은 [행, 열] 순서대로 지정할 수 있다.
# 행과 열을 0~1까지 슬라이싱
print('array2d[0:2, 0:2] \n', array2d[0:2,0:2])
# 행은 1~2까지, 열은 0~2까지 슬라이싱
print('array2d[1:3, 0:3] \n', array2d[1:3,0:3])
print('array2d[1:3, :] \n', array2d[1:3,:])
print('array2d[:, :] \n', array2d[:,:])
print('array2d[:2, 1:] \n', array2d[:2,1:])
print('array2d[:2, 0] \n', array2d[:2,0])



# 행 전체를 슬라이싱 할때는 행 인덱스만 사용하면 된다.
print('0행 전체', array2d[0])
print('1행 전체', array2d[1])
print('array2d[0] shape', array2d[0].shape)

# 열 전체를 슬라이싱 할때는 행도 함께 표현해야 한다.
# 행, 열 순서로 지정해야 하므로 행을 생략할 수 없다.
print('0열 전체',array2d[:,0])
print('2열 전체',array2d[:,2])