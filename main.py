import cv2
import time
from hand_tracker import HandTracker
from effects import draw_glowing_line, draw_glowing_circle, rainbow_color, draw_hud_text
from gesture import detect_gesture, get_spread_percent

def main():
    tracker = HandTracker(max_hands=2)
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    prev_time = 0
    print("HandConnect Running... Press 'Q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Webcam error!")
            break

        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]

        # Dark background for glow effect
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
        frame = cv2.addWeighted(frame, 0.2, overlay, 0.8, 0)

        landmarks_list = tracker.get_landmarks(frame)
        hands_detected = 0
        all_hands_points = []

        if landmarks_list:
            hands_detected = len(landmarks_list)

            for hand_landmarks in landmarks_list:
                points = tracker.get_pixel_points(hand_landmarks, w, h)
                if not points:
                    continue

                all_hands_points.append(points)

                gesture = detect_gesture(points)
                spread  = get_spread_percent(points)

                # Intra-hand rainbow lines
                for i, (start_idx, end_idx) in enumerate(tracker.CONNECTIONS):
                    color = rainbow_color(i, len(tracker.CONNECTIONS))
                    draw_glowing_line(frame,
                                      points[start_idx],
                                      points[end_idx],
                                      color,
                                      thickness=2)

                # Landmark dots
                for pt in points:
                    draw_glowing_circle(frame, pt, radius=5)

                draw_hud_text(frame, f"Gesture: {gesture}", (10, 80))
                draw_hud_text(frame, f"Spread:  {spread}%", (10, 110))

            # Inter-hand lines — dono haathon ke beech
            if len(all_hands_points) == 2:
                hand1 = all_hands_points[0]
                hand2 = all_hands_points[1]

                fingertip_pairs = [(4,4),(8,8),(12,12),(16,16),(20,20)]

                for i, (idx1, idx2) in enumerate(fingertip_pairs):
                    color = rainbow_color(i, len(fingertip_pairs))
                    draw_glowing_line(frame,
                                      hand1[idx1],
                                      hand2[idx2],
                                      color,
                                      thickness=3)

                # Wrist to wrist
                draw_glowing_line(frame, hand1[0], hand2[0],
                                  (255, 255, 255), thickness=2)

        # FPS
        curr_time = time.time()
        fps = int(1 / (curr_time - prev_time + 0.001))
        prev_time = curr_time

        draw_hud_text(frame, f"Hands Detected: {hands_detected}", (10, 30))
        draw_hud_text(frame, f"FPS: {fps}", (10, 55))
        draw_hud_text(frame, "Press Q to quit", (w-180, 30), color=(100, 100, 255))

        cv2.imshow("HandConnect - AR Hand Tracker", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Closed.")

if __name__ == "__main__":
    main()