import os
import shutil
import random

base = r"D:\dullnessdetect"

images = []
labels = []

# Collect valid image-label pairs
for file in os.listdir(base):
    if file.endswith((".jpg", ".png", ".jpeg")):
        txt = file.rsplit(".", 1)[0] + ".txt"
        if os.path.exists(os.path.join(base, txt)):
            images.append(file)
            labels.append(txt)

# Shuffle dataset
combined = list(zip(images, labels))
random.shuffle(combined)

split = int(0.8 * len(combined))
train_data = combined[:split]
val_data = combined[split:]

# Create folders
dirs = [
    "images/train", "images/val",
    "labels/train", "labels/val"
]

for d in dirs:
    os.makedirs(os.path.join(base, d), exist_ok=True)

# Move files
def move(data, img_dest, label_dest):
    for img, txt in data:
        shutil.copy(os.path.join(base, img), os.path.join(base, img_dest, img))
        shutil.copy(os.path.join(base, txt), os.path.join(base, label_dest, txt))

move(train_data, "images/train", "labels/train")
move(val_data, "images/val", "labels/val")

print("Dataset split done!")

# -------------------------------
# FIX LABELS (UPDATED)
# -------------------------------

for folder in ["labels/train", "labels/val"]:
    folder_path = os.path.join(base, folder)

    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)

        with open(path, "r") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()

            # ✅ YOUR LOGIC
            if "dull" in file.lower():
                parts[0] = "0"   # Dullness
            else:
                parts[0] = "1"   # Normal

            new_lines.append(" ".join(parts))

        with open(path, "w") as f:
            f.write("\n".join(new_lines))

print("Labels fixed (0=Dullness, 1=Normal)")