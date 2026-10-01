"""
main.py
The Shy Cursor — the OS cursor tries to escape your hand.
"""

import cv2
import pyautogui
import time
from hand_tracker import HandTracker
from cursor_ai import ShyCursor
from ui import draw_hud


SCREEN_W, SCREEN_H = pyautogui.size()


def main():
    tracker = HandTracker()
    cursor = ShyCursor(SCREEN_W, SCREEN_H)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("Cannot open webcam.")
        return

    print("Shy Cursor is running.")
    print(f"Screen: {SCREEN_W}x{SCREEN_H}")
    print("Move your index finger to chase the cursor.")
    print("Press Q in the debug window to quit.\n")

    pyautogui.FAILSAFE = False

    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            break

        frame = cv2.flip(frame, 1)

        fingertip_frame, frame, _ = tracker.find_index_finger(frame)

        finger_screen = None
        if fingertip_frame is not None:
            fh, fw = frame.shape[:2]
            finger_screen = (
                int((fingertip_frame[0] / fw) * SCREEN_W),
                int((fingertip_frame[1] / fh) * SCREEN_H)
            )

        cursor_x, cursor_y = cursor.update(finger_screen)

        try:
            pyautogui.moveTo(cursor_x, cursor_y, duration=0, _pause=False)
        except pyautogui.FailSafeException:
            pass

        frame = draw_hud(frame, cursor.get_mood(), fingertip_frame)
        cv2.imshow("Shy Cursor — Debug", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.008)

    cap.release()
    tracker.close()
    cv2.destroyAllWindows()
    print("Shy Cursor stopped.")


if __name__ == "__main__":
    main()