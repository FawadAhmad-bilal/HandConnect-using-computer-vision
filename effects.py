import cv2
import numpy as np

def rainbow_color(index, total):
    hue = int((index / total) * 180)
    hsv = np.uint8([[[hue, 255, 255]]])
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0][0]
    return tuple(int(x) for x in bgr)

def draw_glowing_line(frame, pt1, pt2, color, thickness=2):
    for i in range(8, 0, -1):
        alpha = i / 8.0
        glow_color = tuple(int(c * alpha) for c in color)
        cv2.line(frame, pt1, pt2, glow_color, thickness * i * 2)
    cv2.line(frame, pt1, pt2, color, thickness * 3)
    cv2.line(frame, pt1, pt2, (255, 255, 255), thickness)

def draw_glowing_circle(frame, center, radius=6, color=(255, 255, 255)):
    for i in range(4, 0, -1):
        alpha = i / 4.0
        glow_color = tuple(int(c * alpha) for c in color)
        cv2.circle(frame, center, radius * i, glow_color, -1)
    cv2.circle(frame, center, radius, (255, 255, 255), -1)

def draw_hud_text(frame, text, pos, color=(0, 255, 180), scale=0.6, thickness=1):
    cv2.putText(frame, text, pos,
                cv2.FONT_HERSHEY_SIMPLEX,
                scale, color, thickness, cv2.LINE_AA)