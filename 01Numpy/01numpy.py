# 넘파이 모듈 임포트 및 별칭 부여 
import numpy as np

'''
ndarray 
  : 넘파이의 기반이 되는 데이터타입. 다차원(Multi-Dimensional) 배열을
  쉽게 생성하고 다양한 연산을 수행한다. 
  ndarray에 저장하는 데이터는 숫자, 문자열, Boolean 등 모두 가능하다.
  단 연산의 특성상 같은 자료형이어야 한다. 
'''

#1차원 배열 : 3행  
array1 = np.array([1, 2, 3])
print('타입1:', type(array1))
print('형태1:', array1.shape)

#2차원 배열 : 2행 3열  
array2 = np.array([[1, 2, 3],
                   [4, 5, 6]])
print('형태2:', array2.shape)

#2차원 배열 : 1행 3열(대괄호가 2개이므로 2차원 배열)
array3 = np.array([[1, 2, 3]])
print('형태3:', array3.shape)

#ndim : 차원 표시
print("array1: {0}차원".format(array1.ndim))
print("array2: %d차원" % array2.ndim)
print("array3: %d차원" % array3.ndim)

