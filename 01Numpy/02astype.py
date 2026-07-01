import numpy as np

# 정수만으로 리스트 생성 
list1 = [1, 2, 3]
# 리스트를 ndarray로 변환 
array1 = np.array(list1)
print('array1 출력:', array1)
# 타입 확인 : ndarray 
print('타입:', type(array1))
# 배열에 저장된 데이터 타입 확인 : int64
print('dtype:', array1.dtype)

# 실수가 포함된 리스트 생성 
list2 = [1, 2, 3.0]
# 배열로 변환시 모든 데이터가 실수로 변환된다. 
array2 = np.array(list2)
print('array2 출력:', array2)
print('타입:', type(array2))
# 실수가 포함되었으므로 float64로 출력됨 
print('dtype:', array2.dtype)

# 문자열이 포함된 리스트 생성 
list3 = [1, 2, 'test']
# 모든 데이터가 문자열로 변환되어 출력됨 
array3 = np.array(list3)
print('array3 출력:', array3)
print('타입:', type(array3))
# <U21 로 출력됨. 유니코드 문자열 데이터 타입을 의미한다. 
print('dtype:', array3.dtype)

# astype() : ndarray의 데이터 타입을 변경하는 함수 
array_int1 = np.array([1, 2, 3])
# 정수형을 실수형으로 변경 
array_float1 = array_int1.astype('float64')
print(array_float1, array_float1.dtype)

# 실수형을 정수형으로 변경 
array_float2 = np.array([1.1, 2.1, 3.1])
array_int2= array_float2.astype('int32')
print(array_int2, array_int2.dtype)


