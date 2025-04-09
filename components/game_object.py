from OpenGL.GL import *
from OpenGL.GLU import *

class GameObject:
    def __init__(self, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
        self.position = list(position)
        self.rotation = list(rotation)
        self.scale = list(scale)
        
    def update(self, delta_time):
        """Update the game object's state"""
        pass
        
    def draw(self):
        """Draw the game object"""
        pass
        
    def apply_transformations(self):
        """Apply position, rotation, and scale transformations"""
        # Apply position
        glTranslatef(self.position[0], self.position[1], self.position[2])
        
        # Apply rotation
        glRotatef(self.rotation[0], 1, 0, 0)  # Pitch
        glRotatef(self.rotation[1], 0, 1, 0)  # Yaw
        glRotatef(self.rotation[2], 0, 0, 1)  # Roll
        
        # Apply scale
        glScalef(*self.scale)
