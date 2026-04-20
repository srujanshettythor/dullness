from ultralytics import YOLO

# Load base model
model = YOLO('yolov8n.pt')

# Train model
model.train(
    data='data.yaml',
    epochs=120,
    imgsz=640,
    batch=8,
    name='chicken_health_model',
    augment=True
)