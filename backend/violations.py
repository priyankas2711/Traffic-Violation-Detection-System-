LINE_Y = 300

def check_stop_line(obj):
    x1, y1, x2, y2 = obj["bbox"]
    if y2 > LINE_Y:
        return True
    return False


def check_wrong_side(prev_x, current_x):
    if current_x < prev_x:  # moving left
        return True
    return False


def check_triple_riding(person_count):
    return person_count >= 3


def check_helmet(person_detected, helmet_detected):
    return person_detected and not helmet_detected