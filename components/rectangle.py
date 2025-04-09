from OpenGL.GL import *
import pygame
from .game_object import GameObject

class Rectangle(GameObject):
    def __init__(self):
        super().__init__()
        self.visible = True
        self.height = 6.0  # Height (Y axis)
        self.width = 8.0  # Width (X axis)
        self.depth = 3.0  # Depth (Z axis)
        self.position = [0.0, -5.0, 0.0]  # Start at floor level
        
    def draw(self):
        if not self.visible:
            return
            
        # Save the current matrix
        glPushMatrix()
        super().apply_transformations()
        
        # Disable lighting for flat color without reflections
        glDisable(GL_LIGHTING)
        
        # Set an even darker gray color
        gray = [0.25, 0.25, 0.25]  # Very dark gray color
        glColor3f(*gray)
        
        # Calculate half dimensions for vertex positions
        half_width = self.width / 2
        half_height = self.height / 2
        half_depth = self.depth / 2
        
        # Draw the rectangle using quads
        glBegin(GL_QUADS)
        
        # Front face
        glNormal3f(0.0, 0.0, 1.0)
        glVertex3f(-half_width, -half_height, half_depth)   # Bottom left
        glVertex3f(half_width, -half_height, half_depth)    # Bottom right
        glVertex3f(half_width, half_height, half_depth)     # Top right
        glVertex3f(-half_width, half_height, half_depth)    # Top left
        
        # Back face
        glNormal3f(0.0, 0.0, -1.0)
        glVertex3f(-half_width, -half_height, -half_depth)  # Bottom left
        glVertex3f(-half_width, half_height, -half_depth)   # Top left
        glVertex3f(half_width, half_height, -half_depth)    # Top right
        glVertex3f(half_width, -half_height, -half_depth)   # Bottom right
        
        # Top face
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(-half_width, half_height, -half_depth)   # Back left
        glVertex3f(-half_width, half_height, half_depth)    # Front left
        glVertex3f(half_width, half_height, half_depth)     # Front right
        glVertex3f(half_width, half_height, -half_depth)    # Back right
        
        # Bottom face
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(-half_width, -half_height, -half_depth)  # Back left
        glVertex3f(half_width, -half_height, -half_depth)   # Back right
        glVertex3f(half_width, -half_height, half_depth)    # Front right
        glVertex3f(-half_width, -half_height, half_depth)   # Front left
        
        # Right face
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f(half_width, -half_height, -half_depth)   # Bottom back
        glVertex3f(half_width, half_height, -half_depth)    # Top back
        glVertex3f(half_width, half_height, half_depth)     # Top front
        glVertex3f(half_width, -half_height, half_depth)    # Bottom front
        
        # Left face
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-half_width, -half_height, -half_depth)  # Bottom back
        glVertex3f(-half_width, -half_height, half_depth)   # Bottom front
        glVertex3f(-half_width, half_height, half_depth)    # Top front
        glVertex3f(-half_width, half_height, -half_depth)   # Top back
        
        glEnd()
        
        # Restore the matrix and re-enable lighting
        glPopMatrix()
        glEnable(GL_LIGHTING)
        
    def toggle(self):
        self.visible = not self.visible
