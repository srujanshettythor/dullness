import os
import shutil
import random

# 📂 Source folder
source_dir = r"D:\dullnessdetect"

# 📂 Destination folders
train_img = r"D:\dullnessdetect\images\train"
val_img = r"D:\dullnessdetect\images\val"
train_lbl = r"D:\dullnessdetect\labels\train"
val_lbl = r"D:\dullnessdetect\labels\val"

# Create folders
for path in [train_img, val_img, train_lbl, val_lbl]:
    os.makedirs(path, exist_ok=True)

# Get all images
images = [f for f in os.listdir(source_dir) if f.endswith((".jpg", ".png", ".jpeg"))]

random.shuffle(images)

split_ratio = 0.8
split_index = int(len(images) * split_ratio)

train_files = images[:split_index]
val_files = images[split_index:]

def move_files(file_list, img_dest, lbl_dest):
    for img in file_list:
        name = os.path.splitext(img)[0]
        txt = name + ".txt"

        img_path = os.path.join(source_dir, img)
        txt_path = os.path.join(source_dir, txt)

        # ✅ Only move if BOTH exist
        if os.path.exists(txt_path):
            shutil.copy(img_path, os.path.join(img_dest, img))
            shutil.copy(txt_path, os.path.join(lbl_dest, txt))
        else:
            print(f"Missing label for {img}")

# Move files
move_files(train_files, train_img, train_lbl)
move_files(val_files, val_img, val_lbl)

print(" Dataset split completed safely!")