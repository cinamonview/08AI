import numpy as np

# 1~9까지의 값으로 1차원 배열 생성 
array1 = np.arange(start=1, stop=10)
print('array1:', array1)

# index는 0부터 시작이므로 세번째 요소 선택 
value = array1[2]
print('value:', value)
print(type(value))

# 인덱스가 음수인 경우 오른쪽부터 접근 
print('맨 뒤의 값:', array1[-1])
print('맨 뒤에서 두번째 값:', array1[-2])

# 인덱스로 접근해서 값 변경 
array1[0] = 9
array1[8] = 0
print('array1:', array1)

# 1차원 배열 생성 후 3행3열인 2차원 배열로 변환 
array1d = np.arange(start=1, stop=10)
array2d = array1d.reshape(3, 3)
# 배열, 배열의 형태, 차원수 출력 
print(array2d, array2d.shape, array2d.ndim)

# 행, 열 인덱스를 통해 요소 접근 
print('(row=0,col=0) index 가리키는 값:', array2d[0, 0])
print('(row=0,col=1) index 가리키는 값:', array2d[0, 1])
print('(row=1,col=0) index 가리키는 값:', array2d[1, 0])
print('(row=2,col=2) index 가리키는 값:', array2d[2, 2])

