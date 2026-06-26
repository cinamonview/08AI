

import numpy as np

# 배열의 정렬 - argsort()

'''
argsort() :
    배열의 원소들을 정렬했을 때의 원래 인덱스를 반환한다.
    즉, 반환된 인덱스를 원본 배열에 적용하면
    정렬된 배열을 얻을 수 있다.
    원소들의 정렬 전 인덱스를 확인하거나, 정렬된 순서를 유지한 채
    원본 배열의 인덱스를 찾을 때 유용하다.
'''

# 원본 배열
org_array = np.array([3,1,9,5])

# 오름차순 정렬 되었을때 원본배열의 인덱스를 반환해준다.
sort_indices = np.argsort(org_array)
# 앞에서의 결과를 적용하면 배열이 오름차순으로 정렬된다
print('타입', type(sort_indices))
print('결과 인덱스1 : ', sort_indices)


# 내림차순 정렬이므로 위와 반대의 결과가 출력된다.
sort_indices_desc = np.argsort(org_array)[::-1]
print('결과 인덱스2 : ', sort_indices_desc)

# 문자열 배열 생성 (학생이름)
name_array = np.array(['John','Mike','Sarah','Kate','Samuel'])
# 정수형 배열 생성 (점수)
score_array = np.array([78,95,84,98,88])
# 점수를 오름차순으로 정렬한 결과 인덱스를 반환
sort_indices_asc = np.argsort(score_array)
print('결과 인덱스3 : ', sort_indices_asc)
# 점수의 결과 인덱스를 이름에 적용하여 성적순으로 정렬한다.
print('성적순으로 이름 출력 : ', name_array[sort_indices_asc])


'''
Numpy의 ndarray는 문자열과 정수를 동시에 요소로 초기화 할 수 없다.
하나의 타입으로만 정의되기 때문에 
점수와 이름은 각각의 배열로 정의해야 한다.
만약 점수를 기준으로 정렬하고 싶다면, 점수 배열의 정렬된 인덱스를
argsort() 함수로 반환받은 후 이름 배열에 적용하면 된다.
'''
