import os

path = '/Users/macintoshhd/Desktop/python/MiniVGGNet/datasets/animals_new/panda'
count = 0

for filename in os.listdir(path):
    if filename.endswith(".jpg"):
        count += 1
print("Số lượng ảnh trong thư mục là:", count)