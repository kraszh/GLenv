from OpenGL.GL import *
from OpenGL.GLU import *
import math

class Camera:
    def __init__(self):
        # Fixed camera position to view the environment
        self.position = [0.0, 5.0, 30.0]    # Further back for better view
        self.target = [0.0, 0.0, 0.0]      # Look at center
        self.up = [0.0, 1.0, 0.0]          # Y is up
        self.min_zoom = 10.0  # Closest we can get
        self.max_zoom = 50.0  # Furthest we can get
        print(f"Camera initialized at position {self.position}")
        
    def update(self, delta_time):
        pass
        
    def apply(self):
        # Set up the camera view
        gluLookAt(
            self.position[0], self.position[1], self.position[2],  # Camera position
            self.target[0], self.target[1], self.target[2],       # Look at point
            self.up[0], self.up[1], self.up[2]                    # Up vector
        )
        
    def handle_scroll(self, y_scroll):
        # Zoom in/out based on scroll amount
        zoom_speed = 2.0
        self.position[2] = max(self.min_zoom, min(self.max_zoom, 
                                                self.position[2] - y_scroll * zoom_speed))
        
    def handle_key(self, key):
        # Zoom with + and - keys
        zoom_amount = 2.0
        if key == b'=':
            self.position[2] = max(self.min_zoom, self.position[2] - zoom_amount)
        elif key == b'-':
            self.position[2] = min(self.max_zoom, self.position[2] + zoom_amount)
