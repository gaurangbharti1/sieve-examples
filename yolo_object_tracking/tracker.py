import sieve
from typing import Dict

metadata = sieve.Metadata(
    description="Tracks objects using the SORT algorithm.",
    code_url="https://github.com/sieve-community/examples/tree/main/yolo_object_tracking/tracker.py",
    tags=["Tracking", "Video"],
    readme=open("README.md", "r").read(),
)


@sieve.function(
    name="sort-tracker",
    gpu=False,
    python_version="3.8",
    iterator_input=True,
    python_packages=["filterpy==1.4.5", "uuid==1.30"],
    metadata=metadata,
)
def SORT(objects: list) -> Dict:
    """
    :param objects: Generator of list of objects with their bounding boxes, classes, and scores
    :return: Tracked objects keyed by object ID
    """

    from sort import Sort
    import numpy as np
    import uuid

    l = []
    for i in objects:
        if len(i) > 0:
            l.append(i)
    sorted_by_frame_number = sorted(l, key=lambda k: k[0]["frame_number"])
    separated_by_class = {}
    for i in sorted_by_frame_number:
        entities = i
        frame_number = i[0]["frame_number"]
        for entity in entities:
            if entity["class_name"] not in separated_by_class:
                separated_by_class[entity["class_name"]] = {}

            if separated_by_class[entity["class_name"]].get(frame_number) is None:
                separated_by_class[entity["class_name"]][frame_number] = []
            separated_by_class[entity["class_name"]][frame_number].append(entity)

    # object id key and object value where object is a list of boxes
    ids = {}
    for i in separated_by_class:
        number_to_uuid = {}
        boxes = []
        mot_tracker = Sort()
        for frame_number in sorted(separated_by_class[i].keys()):
            for box in separated_by_class[i][frame_number]:
                boxes.append(
                    [
                        box["box"][0],
                        box["box"][1],
                        box["box"][2],
                        box["box"][3],
                        box["score"],
                    ]
                )
            if len(boxes) == 0:
                boxes = np.empty((0, 5))
            else:
                boxes = np.array(boxes)
            trackers = mot_tracker.update(boxes)
            for d in trackers:
                if d[4] not in number_to_uuid:
                    number_to_uuid[d[4]] = str(uuid.uuid4())
                if number_to_uuid[d[4]] not in ids:
                    ids[number_to_uuid[d[4]]] = []
                ids[number_to_uuid[d[4]]].append(
                    {
                        "frame_number": frame_number,
                        "box": [d[0], d[1], d[2], d[3]],
                        "class": i,
                    }
                )
            boxes = []

    yield ids
