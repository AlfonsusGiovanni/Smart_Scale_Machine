my_array = [[0]*5 for _ in range(5)]

print(f"length: {len(my_array)}")

num_counter = 0
for i in range(0, 5):
    for j in range(0, 5):
        num_counter+=1
        my_array[i][j] = num_counter
        print(f"num:{num_counter} | array:{my_array[i][j]}")

print(my_array)