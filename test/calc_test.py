#Kode untuk tiap produk
product_item = ["Tepung A", "Tepung B", "Tepung Campur", "Jagung"]

items_data = [[product_item[0], 10], [product_item[1], 5], [product_item[2], 0]]

items_count = len(items_data)
print(f"Item Count: {items_count}")

item_type = [0]*items_count
item_weight = [0]*items_count

for i in range(0, items_count):
    item_type[i] = items_data[i][0]
    item_weight[i] = items_data[i][1]

print(item_type)
print(item_weight)