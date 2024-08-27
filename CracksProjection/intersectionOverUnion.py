def calculate_iou(box1, box2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters:
    box1, box2: Tuples containing the coordinates of the bounding boxes in the format:
                (x1, y1, x2, y2) where
                (x1, y1) is the top-left corner,
                (x2, y2) is the bottom-right corner.

    Returns:
    iou: The IoU of the two bounding boxes.
    """
    
    # Unpack the coordinates of the bounding boxes
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2

    # Compute the coordinates of the intersection rectangle
    inter_min_x = max(x1_min, x2_min)
    inter_min_y = max(y1_min, y2_min)
    inter_max_x = min(x1_max, x2_max)
    inter_max_y = min(y1_max, y2_max)

    # Compute the width and height of the intersection rectangle
    inter_width = inter_max_x - inter_min_x
    inter_height = inter_max_y - inter_min_y

    # If there is no overlap, IoU is 0
    if inter_width <= 0 or inter_height <= 0:
        return 0.0

    # Compute the area of the intersection rectangle
    inter_area = inter_width * inter_height

    # Compute the area of both bounding boxes
    box1_area = (x1_max - x1_min) * (y1_max - y1_min)
    box2_area = (x2_max - x2_min) * (y2_max - y2_min)

    # Compute the area of the union
    union_area = box1_area + box2_area - inter_area

    # Compute the IoU
    iou = inter_area / union_area

    return iou
