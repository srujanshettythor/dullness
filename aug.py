import os
import cv2
import random

# Paths
img_dirs = [
    r"D:\dullnessdetect\images\train",
    r"D:\dullnessdetect\images\val"
]

lbl_dirs = [
    r"D:\dullnessdetect\labels\train",
    r"D:\dullnessdetect\labels\val"
]

def augment_image(img, labels):
    h, w = img.shape[:2]

    # Flip horizontally
    if random.random() < 0.5:
        img = cv2.flip(img, 1)
        new_labels = []
        for l in labels:
            cls, x, y, bw, bh = l
            x = 1 - x
            new_labels.append([cls, x, y, bw, bh])
        labels = new_labels

    # Brightness change
    if random.random() < 0.5:
        value = random.randint(-30, 30)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = cv2.add(hsv[:, :, 2], value)
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return img, labels


for img_dir, lbl_dir in zip(img_dirs, lbl_dirs):
    for file in os.listdir(img_dir):
        if file.endswith((".jpg", ".png", ".jpeg")):

            img_path = os.path.join(img_dir, file)
            txt_path = os.path.join(lbl_dir, file.replace(".jpg", ".txt").replace(".png", ".txt").replace(".jpeg", ".txt"))

            if not os.path.exists(txt_path):
                continue

            img = cv2.imread(img_path)

            # Read labels
            labels = []
            with open(txt_path, "r") as f:
                for line in f:
                    labels.append(list(map(float, line.strip().split())))

            # Augment
            aug_img, aug_labels = augment_image(img, labels)

            # Save new image
            new_name = "aug_" + file
            cv2.imwrite(os.path.join(img_dir, new_name), aug_img)

            # Save new label
            with open(os.path.join(lbl_dir, new_name.replace(".jpg", ".txt").replace(".png", ".txt").replace(".jpeg", ".txt")), "w") as f:
                for l in aug_labels:
                    f.write(" ".join(map(str, l)) + "\n")

print("Augmentation completed!")