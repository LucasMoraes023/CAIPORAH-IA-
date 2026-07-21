from typing import Any

import cv2
import numpy as np
from mss import mss

class VisionEngine:
    def __init__(self) -> None:
        self.active = False

    def start(self) -> None:
        self.active = True

    def stop(self) -> None:
        self.active = False

    def status(self) -> str:
        return 'active' if self.active else 'stopped'

    def capture_screen(self) -> Any:
        try:
            with mss() as sct:
                frame = np.array(sct.grab(sct.monitors[1]))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                return frame
        except Exception:
            return None

    def analyze_frame(self, frame: Any = None) -> dict:
        if frame is None:
            frame = self.capture_screen()

        if frame is None:
            return {
                'hud': None,
                'minimap': None,
                'health_bar': None,
                'energy_bar': None,
                'events': [],
                'message': 'Não foi possível capturar a tela.',
            }

        height, width = frame.shape[:2]

        # Edge-based metrics (simple activity indicator)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        edge_count = int(np.sum(edges > 0))

        # Convert to HSV for color segmentation
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        def pct_mask(h_low, s_low, v_low, h_high, s_high, v_high, region=None):
            mask = cv2.inRange(hsv, (h_low, s_low, v_low), (h_high, s_high, v_high))
            if region is not None:
                x, y, w, h = region
                sub = mask[y:y+h, x:x+w]
                return int(100.0 * (np.count_nonzero(sub) / (w * h)))
            return int(100.0 * (np.count_nonzero(mask) / (hsv.shape[0] * hsv.shape[1])))

        # Heuristics: health bar often red/orange at top-left area
        hw = int(width * 0.35)
        hh = int(height * 0.12)
        health_region = (0, 0, hw, hh)
        # red ranges (two ranges for HSV red wrap)
        health_pct1 = pct_mask(0, 100, 50, 10, 255, 255, region=health_region)
        health_pct2 = pct_mask(160, 100, 50, 179, 255, 255, region=health_region)
        health_pct = max(health_pct1, health_pct2)

        # Energy bar / mana often blue/cyan near health or bottom; check top region
        energy_pct = pct_mask(90, 60, 50, 140, 255, 255, region=health_region)

        # Minimap detection: look for circular area at bottom-left or top-right
        minimap_found = False
        mm_region = frame[int(height*0.6):int(height*0.95), 0:int(width*0.35)]
        mm_gray = cv2.cvtColor(mm_region, cv2.COLOR_BGR2GRAY)
        mm_blur = cv2.GaussianBlur(mm_gray, (7,7), 0)
        circles = cv2.HoughCircles(mm_blur, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=200)
        if circles is not None:
            minimap_found = True

        return {
            'hud': {
                'health_percent_region': health_region,
            },
            'minimap': {
                'found': minimap_found,
            },
            'health_bar': {
                'approx_percent_color': health_pct,
            },
            'energy_bar': {
                'approx_percent_color': energy_pct,
            },
            'events': [],
            'screen': {
                'width': width,
                'height': height,
                'edge_pixels': edge_count,
            },
        }
