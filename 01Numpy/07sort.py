import numpy as np

''' 
sort() 
    : 배열의 요소를 정렬된 상태로 반환해주는 함수. 오름차순 정렬이 
    디폴트 값. 원본 배열은 그대로 유지한채로 정렬된 복사본을 반환한다. 
    형식] np.sort(원본배열, axis=정렬할축, kind=정렬알고리즘)
'''
# 배열 생성 
org_array = np.array([3, 1, 9, 5])
print('원본배열:', org_array)

# Numpy를 통해 sort()를 호출하면 원본은 그대로 유지된다. 
sort_array1 = np.sort(org_array)
print('원본', org_array)
print('복사본1', sort_array1)

# 배열을 이용해서 sort() 함수를 직접 호출하면 원본이 변경된다. 
sort_array2 = org_array.sort()
print('변경된원본', org_array)
# 원본이 변경되므로 복사본은 반환되지 않아 None이 출력됨. 
print('복사본2', sort_array2)

''' 
슬라이싱 문법 [start:stop:step] 에서 step만 -1로 설정하면 배열을
역방향으로 순회하라는 의미로 사용된다. 이 경우 start가 마지막 인덱스가
되고 stop이 시작인덱스가 된다. 
'''
sort_array1_desc = np.sort(org_array)[::-1]
print('내림차순정렬', sort_array1_desc)

# 2차원 배열 생성 
array2d = np.array([[8, 12],
                   [7, 1]])
# Row(행) 방향으로 정렬 
sort_array2d_axis0 = np.sort(array2d, axis=0)
print(sort_array2d_axis0)

# Column(열) 방향으로 정렬 
sort_array2d_axis1 = np.sort(array2d, axis=1)
print(sort_array2d_axis1)

