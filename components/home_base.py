from OpenGL.GL import *
from OpenGL.GLU import *
from .game_object import GameObject

import math

class HomeBase(GameObject):
    def __init__(self, color=(1.0, 0.0, 0.0), size=2):  # Default red color
        super().__init__()
        self.color = color
        self.size = size
        self.segments = 32  # Number of segments for the circle
        
    def draw(self):
        glDisable(GL_LIGHTING)
        
        # Platform color (slightly darker than flag)
        platform_color = [c * 0.7 for c in self.color]
        glColor3f(*platform_color)
        
        # Draw circular platform
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, 0)  # Center point
        for i in range(self.segments + 1):
            angle = 2.0 * math.pi * i / self.segments
            x = self.size * math.cos(angle)
            z = self.size * math.sin(angle)
            glVertex3f(x, 0, z)
        glEnd()
        
        # Draw platform outline
        glLineWidth(2.0)
        glColor3f(0.0, 0.0, 0.0)  # Black outline
        glBegin(GL_LINE_LOOP)
        for i in range(self.segments):
            angle = 2.0 * math.pi * i / self.segments
            x = self.size * math.cos(angle)
            z = self.size * math.sin(angle)
            glVertex3f(x, 0, z)
        glEnd()
        
        glEnable(GL_LIGHTING)
