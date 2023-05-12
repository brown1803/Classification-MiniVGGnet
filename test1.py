import os
import argparse
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import img_to_array,load_img
import numpy as np
import shutil


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="Đường dẫn dataset ban đầu")
ap.add_argument("-o", "--output", required=True, help="Đường dẫn dataset mới để lưu trữ ảnh tăng cường")
ap.add_argument("-p", "--prefix", type=str, default="image", help="Tiền tố output đã tăng cường")
args = vars(ap.parse_args())  

for class_name in os.listdir(args["input"]):
    class_path = os.path.join(args["output"], class_name)
    os.makedirs(class_path, exist_ok=True)

for class_name in os.listdir(args["input"]):
    class_path = os.path.join(args["input"], class_name)
    augmented_class_path = os.path.join(args["output"], class_name)
    for file_name in os.listdir(class_path):
        src_path = os.path.join(class_path, file_name)
        dest_path = os.path.join(augmented_class_path, file_name)
        shutil.copy(src_path, dest_path)

def augmentation(image_path, save_folder,num_aug):
    print("[INFO] Nạp image...")
    image = load_img(image_path)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    aug = ImageDataGenerator(rescale=1./255, rotation_range=40, width_shift_range=0.2, height_shift_range=0.2,
                            shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode='nearest')
    total = 0

    print("[INFO] generating images...")
    imageGen = aug.flow(image, batch_size=1, save_to_dir=save_folder, save_prefix=args["prefix"], save_format="jpg")

    image_augmentation = []
   
    for image in imageGen:
        # image = next(imageGen)
        total = total + 1
        image_augmentation.append(image)
    # while total <= num_aug:
    #     image = next(imageGen)
    #     total += 1
    #     image_augmentation.append(image)
        if total == num_aug+1: 
            break

    return image_augmentation

nums = 10
num_aug = 50



for class_name in os.listdir(args["output"]):

    file_list = []
    print(class_name)
    
    class_name_path = os.path.join(args["output"],class_name)

    for img_path in os.listdir(class_name_path):
        file_list.append(os.path.join(class_name_path,img_path))

    selected_file = file_list[:nums]

    for img_aug in selected_file:
        augmentation(img_aug,class_name_path,num_aug)
    
    for class_name in os.listdir(args["output"]):
        class_path = os.path.join(args["output"], class_name)
        num_images = len(os.listdir(class_path))
        if num_images > 1500:
            excess_images = num_images - 1500
            for i in range(excess_images):
                os.remove(os.path.join(class_path, os.listdir(class_path)[i]))



 
