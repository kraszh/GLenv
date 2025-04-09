from OpenGL.GL import *
from OpenGL.GLU import *
from .game_object import GameObject

class Flag(GameObject):
    def __init__(self, color=(1.0, 0.0, 0.0), size=0.5):  # Default red color
        super().__init__()
        self.color = color
        self.size = size
        self.home_position = [0, 0, 0]  # Store original position
        
    def set_home_position(self, position):
        self.home_position = position.copy()
        self.position = position.copy()
        
    def reset_position(self):
        self.position = self.home_position.copy()
        
    def draw(self):
        pole_height = self.size * 3
        pole_width = self.size * 0.05
        
        # Draw flag pole
        glDisable(GL_LIGHTING)
        glColor3f(0.7, 0.7, 0.7)  # Gray pole
        glBegin(GL_QUADS)
        # Front
        glVertex3f(-pole_width, 0, -pole_width)
        glVertex3f(pole_width, 0, -pole_width)
        glVertex3f(pole_width, pole_height, -pole_width)
        glVertex3f(-pole_width, pole_height, -pole_width)
        # Back
        glVertex3f(-pole_width, 0, pole_width)
        glVertex3f(pole_width, 0, pole_width)
        glVertex3f(pole_width, pole_height, pole_width)
        glVertex3f(-pole_width, pole_height, pole_width)
        # Left
        glVertex3f(-pole_width, 0, -pole_width)
        glVertex3f(-pole_width, 0, pole_width)
        glVertex3f(-pole_width, pole_height, pole_width)
        glVertex3f(-pole_width, pole_height, -pole_width)
        # Right
        glVertex3f(pole_width, 0, -pole_width)
        glVertex3f(pole_width, 0, pole_width)
        glVertex3f(pole_width, pole_height, pole_width)
        glVertex3f(pole_width, pole_height, -pole_width)
        glEnd()
        
        # Draw flag
        flag_width = self.size * 1.5
        flag_height = self.size
        
        glColor3f(*self.color)  # Flag color
        glBegin(GL_TRIANGLES)
        # Flag (triangle)
        glVertex3f(pole_width, pole_height * 0.8, 0)  # Top of pole
        glVertex3f(pole_width + flag_width, pole_height * 0.8 - flag_height/2, 0)  # Tip
        glVertex3f(pole_width, pole_height * 0.8 - flag_height, 0)  # Bottom of pole
        glEnd()
        
        # Draw flag outline
        glLineWidth(2.0)
        glColor3f(0.0, 0.0, 0.0)  # Black outline
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_TRIANGLES)
        glVertex3f(pole_width, pole_height * 0.8, 0)
        glVertex3f(pole_width + flag_width, pole_height * 0.8 - flag_height/2, 0)
        glVertex3f(pole_width, pole_height * 0.8 - flag_height, 0)
        glEnd()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        glEnable(GL_LIGHTING)
