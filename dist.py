import os

label_paths = [
    r"D:\dullnessdetect\labels\train",
    r"D:\dullnessdetect\labels\val"
]

count = {0: 0, 1: 0}

for label_path in label_paths:
    for file in os.listdir(label_path):
        if file.endswith(".txt"):
            with open(os.path.join(label_path, file)) as f:
                for line in f:
                    cls = int(float(line.split()[0]))  # ✅ FIXED
                    count[cls] += 1

print(count)