from ultralytics import YOLO

model = YOLO("yolov8n.pt")

VEHICLE_CLASSES = [2, 3, 5, 7]  # car, bike, bus, truck
PERSON_CLASS = 0

def detect_objects(frame):
    results = model(frame)[0]
    detections = []

    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        detections.append({
            "class": cls,
            "conf": conf,
            "bbox": (x1, y1, x2, y2)
        })

    return detections