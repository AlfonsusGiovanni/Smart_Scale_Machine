array1d = [1,2,3,4,5] # kolom 1-5
array2d = [[1,2,3,4,5], [1,2,3,4,5]] # baris 1 (kolom 1-5), baris 2 (kolom 1-5)
array3d = [[[1,2,3,4,5], [4,5,6,7,8]], [[9,10,11,12,13], [14,15,16,17,18]]]

test_array = [[[0]*5 for r in range(500)] for s in range(4)] # 4 sheet, 500 kolom, 5 baris

print(f"Sheet count     : {len(test_array)}")
print(f"Row count       : {len(test_array[0])}")
print(f"Column count    : {len(test_array[0][0])}")

print("")

print(array3d[0][1][2]) # Sheet 1 - Row 2 - Column 3
