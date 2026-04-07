import cv2
import time
from detector import detect_objects
from tracker import assign_ids
from utils import save_violation

# ---------------- GLOBAL ----------------
last_saved_time = {}
COOLDOWN = 3
LINE_Y = 380

# ---------------- HELPER ----------------
def is_inside(person, bike):
    px1, py1, px2, py2 = person
    bx1, by1, bx2, by2 = bike

    # overlap check
    if px2 < bx1 or px1 > bx2:
        return False
    if py2 < by1 or py1 > by2:
        return False

    return True

# ---------------- MAIN ----------------
def process_webcam():
    print("🚀 Starting Camera...")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not working")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))

        detections = detect_objects(frame)
        objects = assign_ids(detections)

        persons = []
        bikes = []
        cars = []

        # ---------------- DETECTION ----------------
        for obj in objects:
            x1, y1, x2, y2 = obj["bbox"]
            cls = obj["class"]

            if (y2 - y1) < 60:
                continue

            cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0),2)

            if cls == 0:
                persons.append((x1,y1,x2,y2))

            elif cls == 3:
                bikes.append((x1,y1,x2,y2))

            elif cls == 2:
                cars.append((x1,y1,x2,y2))

        # ================================
        # 🚫 STOP LINE (VEHICLES ONLY)
        # ================================
        for v in bikes + cars:
            x1,y1,x2,y2 = v
            center_y = (y1 + y2)//2

            if center_y > LINE_Y:
                now = time.time()

                if now - last_saved_time.get("stop",0) > COOLDOWN:
                    cv2.putText(frame, "STOP LINE VIOLATION", (x1,y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)

                    save_violation(frame, "stop_line")
                    last_saved_time["stop"] = now

        # ================================
        # 🚧 RESTRICTED ZONE
        # ================================
        for v in bikes + cars:
            x1,y1,x2,y2 = v

            if x1 < 60:
                now = time.time()

                if now - last_saved_time.get("zone",0) > COOLDOWN:
                    cv2.putText(frame, "RESTRICTED ZONE", (x1,y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)

                    save_violation(frame, "restricted_zone")
                    last_saved_time["zone"] = now

        # ================================
        # 👨‍👨‍👦 TRIPLE RIDING (ONLY BIKE)
        # ================================
        for bike in bikes:
            count = 0

            for p in persons:
                if is_inside(p, bike):
                    count += 1

            if count >= 2:
                now = time.time()

                if now - last_saved_time.get("triple",0) > COOLDOWN:
                    bx1,by1,_,_ = bike

                    cv2.putText(frame, "TRIPLE RIDING", (bx1,by1-10),
                                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

                    save_violation(frame, "triple_riding")
                    last_saved_time["triple"] = now

        # ================================
        # 🪖 HELMET (FIXED)
        # ================================
        for bike in bikes:
            bx1,by1,bx2,by2 = bike

            for p in persons:
                if is_inside(p, bike):

                    px1,py1,px2,py2 = p

                    # head region (top 30%)
                    if py1 < (by1 + (by2 - by1)*0.3):

                        now = time.time()

                        if now - last_saved_time.get("helmet",0) > COOLDOWN:
                            cv2.putText(frame, "NO HELMET", (px1,py1-10),
                                        cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),2)

                            save_violation(frame, "no_helmet")
                            last_saved_time["helmet"] = now

        # ---------------- DRAW LINE ----------------
        cv2.line(frame, (0, LINE_Y), (640, LINE_Y), (255,0,0), 2)

        cv2.imshow("🚦 Traffic AI (FINAL)", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# ---------------- RUN ----------------
if __name__ == "__main__":
    process_webcam()