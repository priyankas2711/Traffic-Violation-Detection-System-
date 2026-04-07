import itertools

id_counter = itertools.count()

tracked_objects = {}

def assign_ids(detections):
    objects = []

    for det in detections:
        obj_id = next(id_counter)
        objects.append({**det, "id": obj_id})

    return objects