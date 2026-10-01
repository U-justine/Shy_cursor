"""
cursor_ai.py
The Shy Cursor's brain: fear, wander, panic, calm.
No machine learning — just physics + a state machine.
"""

import numpy as np


FEAR_RADIUS_PX       = 250
MAX_FLEE_SPEED       = 90
CALM_WANDER_SPEED    = 1.5
FRICTION             = 0.85
CALM_AFTER_FRAMES    = 480
PANIC_DIST_FRACTION  = 0.5
CATCH_RADIUS_PX      = 30
FROZEN_FRAMES        = 120


class ShyCursor:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.x = screen_w / 2
        self.y = screen_h / 2
        self.vx = 0.0
        self.vy = 0.0

        self.mood = "calm"
        self.frames_since_threat = 0
        self.frozen_timer = 0
        self.wander_angle = np.random.uniform(0, 2 * np.pi)
        self.wander_change_timer = 0

    def update(self, finger_screen):
        if self.mood == "frozen":
            self.frozen_timer -= 1
            if self.frozen_timer <= 0:
                self._teleport_and_startle()
            return self._apply_physics()

        if finger_screen is not None:
            dx = self.x - finger_screen[0]
            dy = self.y - finger_screen[1]
            dist = np.hypot(dx, dy)

            if dist < CATCH_RADIUS_PX:
                self._on_caught()
                return self._apply_physics()

            if dist < FEAR_RADIUS_PX:
                self._flee(dx, dy, dist)
                self.frames_since_threat = 0
                self.mood = (
                    "panicked"
                    if dist < FEAR_RADIUS_PX * PANIC_DIST_FRACTION
                    else "wary"
                )
            else:
                self.frames_since_threat += 1
                self._wander()
        else:
            self.frames_since_threat += 1
            self._wander()

        if self.frames_since_threat > CALM_AFTER_FRAMES:
            self.mood = "calm"

        return self._apply_physics()

    def _flee(self, dx, dy, dist):
        fear = 1.0 - (dist / FEAR_RADIUS_PX)
        fear = max(0.15, fear)
        speed = MAX_FLEE_SPEED * fear

        nx = dx / (dist + 1e-6)
        ny = dy / (dist + 1e-6)

        jitter_x = np.random.uniform(-0.3, 0.3)
        jitter_y = np.random.uniform(-0.3, 0.3)

        self.vx += (nx + jitter_x) * speed
        self.vy += (ny + jitter_y) * speed

    def _wander(self):
        self.wander_change_timer += 1
        if self.wander_change_timer > 90:
            self.wander_angle += np.random.uniform(-0.6, 0.6)
            self.wander_change_timer = 0

        self.vx += np.cos(self.wander_angle) * CALM_WANDER_SPEED * 0.3
        self.vy += np.sin(self.wander_angle) * CALM_WANDER_SPEED * 0.3

    def _on_caught(self):
        self.mood = "frozen"
        self.frozen_timer = FROZEN_FRAMES
        self.vx = 0.0
        self.vy = 0.0

    def _teleport_and_startle(self):
        self.x = np.random.uniform(200, self.screen_w - 200)
        self.y = np.random.uniform(200, self.screen_h - 200)
        self.vx = np.random.uniform(-40, 40)
        self.vy = np.random.uniform(-40, 40)
        self.mood = "panicked"
        self.frames_since_threat = 0

    def _apply_physics(self):
        self.vx *= FRICTION
        self.vy *= FRICTION

        self.x += self.vx
        self.y += self.vy

        margin = 20
        if self.x < margin:
            self.x = margin
            self.vx = abs(self.vx) * 0.6
        elif self.x > self.screen_w - margin:
            self.x = self.screen_w - margin
            self.vx = -abs(self.vx) * 0.6

        if self.y < margin:
            self.y = margin
            self.vy = abs(self.vy) * 0.6
        elif self.y > self.screen_h - margin:
            self.y = self.screen_h - margin
            self.vy = -abs(self.vy) * 0.6

        return int(self.x), int(self.y)

    def get_mood(self):
        return self.mood