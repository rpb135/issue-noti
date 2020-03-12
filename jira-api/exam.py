import numpy as np

liA = ['111', '222']
liB = ['111']

key = '222'
bl = np.array_equal(liA, liB)
print (bl)
if key in liA:
    print("A 리스트에 해당 값 존재 : ", liA)
elif not np.array_equal(liA, liB) and liB:
    print("A,B 리스트 는 비어 있지 않으며 다르다, liB 는 요소가 존재 함")