"""
ui.py
Debug view: shows webcam + fingertip + cursor mood.
"""

import cv2

BG_DARK     = (22, 22, 22)
TEXT_WHITE  = (255, 255, 255)
ACCENT      = (0, 220, 255)

MOOD_COLORS = {
    "calm":     (120, 220, 120),
    "wary":     (0, 200, 255),
    "panicked": (0, 60, 255),
    "frozen":   (200, 200, 200),
}


def draw_hud(frame, mood, finger_pos):
    h, w, _ = frame.shape
    cv2.rectangle(frame, (0, 0), (w, 55), BG_DARK, -1)

    cv2.putText(frame, "SHY CURSOR", (15, 38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.85, ACCENT, 2, cv2.LINE_AA)

    mood_text = f"MOOD: {mood.upper()}"
    color = MOOD_COLORS.get(mood, TEXT_WHITE)
    cv2.putText(frame, mood_text, (w // 2 - 100, 38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.85, color, 2, cv2.LINE_AA)

    cv2.putText(frame, "Q: quit", (w - 110, 38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1, cv2.LINE_AA)

    if finger_pos is not None:
        cv2.circle(frame, finger_pos, 12, (0, 255, 255), -1)
        cv2.circle(frame, finger_pos, 22, (0, 255, 255), 2)

    return frame