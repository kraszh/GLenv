from OpenGL.GL import *
from OpenGL.GLU import *
from .game_object import GameObject

class DividerWall(GameObject):
    def __init__(self, height=10.0, depth=18.0, thickness=0.005):
        super().__init__()
        self.height = height
        self.depth = depth
        self.thickness = thickness
        self.color = (0.0, 0.7, 1.0, 0.03)  # Light blue with very high transparency
        self.position = [0, -5, 0]  # Move wall down to floor level
        
    def draw(self):
        glPushMatrix()
        self.apply_transformations()
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_LIGHTING)
        
        # Draw translucent wall faces
        glColor4f(*self.color)
        glBegin(GL_QUADS)
        
        # Front face
        glVertex3f(-self.thickness/2, 0, -self.depth/2)
        glVertex3f(self.thickness/2, 0, -self.depth/2)
        glVertex3f(self.thickness/2, self.height, -self.depth/2)
        glVertex3f(-self.thickness/2, self.height, -self.depth/2)
        
        # Back face
        glVertex3f(-self.thickness/2, 0, self.depth/2)
        glVertex3f(self.thickness/2, 0, self.depth/2)
        glVertex3f(self.thickness/2, self.height, self.depth/2)
        glVertex3f(-self.thickness/2, self.height, self.depth/2)
        
        # Right face
        glVertex3f(self.thickness/2, 0, -self.depth/2)
        glVertex3f(self.thickness/2, 0, self.depth/2)
        glVertex3f(self.thickness/2, self.height, self.depth/2)
        glVertex3f(self.thickness/2, self.height, -self.depth/2)
        
        # Left face
        glVertex3f(-self.thickness/2, 0, -self.depth/2)
        glVertex3f(-self.thickness/2, 0, self.depth/2)
        glVertex3f(-self.thickness/2, self.height, self.depth/2)
        glVertex3f(-self.thickness/2, self.height, -self.depth/2)
        
        # Top face
        glVertex3f(-self.thickness/2, self.height, -self.depth/2)
        glVertex3f(self.thickness/2, self.height, -self.depth/2)
        glVertex3f(self.thickness/2, self.height, self.depth/2)
        glVertex3f(-self.thickness/2, self.height, self.depth/2)
        glEnd()
        
        # Draw outline with thick black lines to match environment box
        glColor3f(0.0, 0.0, 0.0)  # Solid black like the box edges
        glLineWidth(4.0)  # Match box edge thickness
        
        # Draw edges
        glBegin(GL_LINES)
        # Vertical edges
        glVertex3f(-self.thickness/2, 0, -self.depth/2)
        glVertex3f(-self.thickness/2, self.height, -self.depth/2)
        
        glVertex3f(self.thickness/2, 0, -self.depth/2)
        glVertex3f(self.thickness/2, self.height, -self.depth/2)
        
        glVertex3f(-self.thickness/2, 0, self.depth/2)
        glVertex3f(-self.thickness/2, self.height, self.depth/2)
        
        glVertex3f(self.thickness/2, 0, self.depth/2)
        glVertex3f(self.thickness/2, self.height, self.depth/2)
        
        # Horizontal edges - top
        glVertex3f(-self.thickness/2, self.height, -self.depth/2)
        glVertex3f(self.thickness/2, self.height, -self.depth/2)
        
        glVertex3f(-self.thickness/2, self.height, self.depth/2)
        glVertex3f(self.thickness/2, self.height, self.depth/2)
        
        # Depth edges - top
        glVertex3f(-self.thickness/2, self.height, -self.depth/2)
        glVertex3f(-self.thickness/2, self.height, self.depth/2)
        
        glVertex3f(self.thickness/2, self.height, -self.depth/2)
        glVertex3f(self.thickness/2, self.height, self.depth/2)
        
        # Horizontal edges - bottom
        glVertex3f(-self.thickness/2, 0, -self.depth/2)
        glVertex3f(self.thickness/2, 0, -self.depth/2)
        
        glVertex3f(-self.thickness/2, 0, self.depth/2)
        glVertex3f(self.thickness/2, 0, self.depth/2)
        
        # Depth edges - bottom
        glVertex3f(-self.thickness/2, 0, -self.depth/2)
        glVertex3f(-self.thickness/2, 0, self.depth/2)
        
        glVertex3f(self.thickness/2, 0, -self.depth/2)
        glVertex3f(self.thickness/2, 0, self.depth/2)
        glEnd()
        
        # Restore states
        glEnable(GL_LIGHTING)
        glDisable(GL_BLEND)
        glPopMatrix()
