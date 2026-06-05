import math

def get_distance(pt1, pt2):
    return math.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)

def detect_gesture(points):
    if not points or len(points) < 21:
        return "Unknown"

    thumb_tip  = points[4]
    index_tip  = points[8]
    middle_tip = points[12]
    ring_tip   = points[16]
    pinky_tip  = points[20]
    wrist      = points[0]

    pinch_dist = get_distance(thumb_tip, index_tip)
    if pinch_dist < 40:
        return "PINCH"

    fingers_open = all(
        get_distance(tip, wrist) > 120
        for tip in [index_tip, middle_tip, ring_tip, pinky_tip]
    )
    if fingers_open:
        return "OPEN HAND"

    return "CLOSED"

def get_spread_percent(points):
    if not points or len(points) < 21:
        return 0
    from gesture import get_distance
    dist = get_distance(points[4], points[20])
    percent = min(int((dist / 300) * 100), 100)
    return percent