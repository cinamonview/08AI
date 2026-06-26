

import numpy as np

'''
fancy indexing : 
    리스트나 ndarray로 인덱스의 집합을 구성하여 요소를 선택하는 인덱싱 방식을 말한다.
    '''


# fancy indexing

array1d = np.arange(start=1, stop=10)
print(array1d)
array2d = array1d.reshape(3,3)
print(array2d)

# 0, 1행을 선택한후 2열 선택
arrayA1 = array2d[[0,1],2]
print('array2d[[0,1],2]=>', arrayA1.tolist())
# 0,1 행 선택후 0~1 열까지 선택
arrayA2 = array2d[[0,1],0:2]
print('array2d[[0,1],0:2]=>', arrayA2.tolist())
# 0행과 1행의 전체 요소 선택. 
# 열은 별도의 지정이 없으므로 전체를 선택하게 된다.
arrayA3 = array2d[[0,1]]
print('array2d[[0,1],2]=>', arrayA3.tolist())


# boolean indexing

'''
Boolean indexing:
    배열의 요소를 True 혹은 False로 표시하는 Boolean 타입의 배열을 생성하고 ,
    이를 인덱스로 사용하여 조건에 만족하는 요소를 선택하거나 
    조작할 수 있는 인덱싱 방식
    '''

# 5를 초과하는 요소들로만 선택하는 조건 생성
# 이 조건만으로 Boolean으로 구성된 배열이 만들어 진다.
print('조건', array1d >5)
# 위 조건으로 만들어진 배열을 적용해서 인덱싱 한다.
arrayB1 = array1d[array1d>5]
print('불린 인덱싱 적용된 결과 : ',arrayB1)

# 앞에서 사용한 조건과 동일하게 리스트를 생성한 후 적용
boolean_indexes = np.array([False,False,False,False,False,True,True,True,True])
arrayB2 = array1d[boolean_indexes]
print('불린 인덱스로 필터링 결과 : ', arrayB2)

# 인덱스 5~8 까지를 지정했으므로 결과는 위와 동일하게 나온다.
indexes = np.array([5,6,7,8])
arrayB3 = array1d[indexes]
print('일반 인덱스로 필터링 결과 : ', arrayB3)
# 즉 결과 1,2,3 은 모두 동일하다

'''
논리연산 : 
    조건을 결합할때는 Numpy의 &,|,~를 사용한다
    Python과 같이 and,or를 사용하면 에러가 발생된다.
'''

# 요소의 값이 짝수이면서, 6을 초과하는 요소만 필터링
arrayB4 = arrayB3[(arrayB3%2 ==0)& (arrayB3>6)]
print('불린 인덱스로 수정 결과 : ', arrayB4)

# 8 이상인 요소들만 0으로 수정
arrayB1[arrayB1 >= 8] = 0
print('불린 인덱스로 수정 결과 :', arrayB1)
