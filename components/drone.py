from OpenGL.GL import *
from OpenGL.GLU import *
from .game_object import GameObject
import math

class Drone(GameObject):
    def __init__(self, color=(1.0, 0.0, 0.0), size=1.0):  # Default red color
        super().__init__()
        self.color = color
        self.size = 0.75  # Fixed size for consistent collision
        self.speed = 0.3  # Slower speed for more precise movement
        self.rotation_speed = 3.0  # Degrees per frame
        self.environment = None  # Will be set by Environment class
        
    def check_rectangle_collision(self, new_x, new_z):
        if not self.environment or not self.environment.rectangle.visible:
            return False
            
        # Get rectangle dimensions and position
        rect = self.environment.rectangle
        rect_x = rect.position[0]
        rect_z = rect.position[2]
        rect_half_width = rect.width / 2
        rect_half_depth = rect.depth / 2
        
        # Add a small buffer around the rectangle to prevent clipping
        buffer = 0.5
        
        # Simple box collision test - if any part of the drone would be inside
        # the rectangle's bounds (plus buffer), prevent movement
        return (rect_x - rect_half_width - buffer <= new_x <= rect_x + rect_half_width + buffer and
                rect_z - rect_half_depth - buffer <= new_z <= rect_z + rect_half_depth + buffer)
    
    def move_forward(self):
        # Calculate new position
        angle_rad = math.radians(self.rotation[1])
        new_x = self.position[0] + math.sin(angle_rad) * self.speed
        new_z = self.position[2] + math.cos(angle_rad) * self.speed
        
        # Check if new position would be within bounds and not colliding with rectangle
        if self.environment:
            half_width = self.environment.width / 2
            half_depth = self.environment.depth / 2
            
            # Only update if within bounds and not colliding
            if (-half_width < new_x < half_width and 
                -half_depth < new_z < half_depth and
                not self.check_rectangle_collision(new_x, new_z)):
                self.position[0] = new_x
                self.position[2] = new_z
        
    def move_backward(self):
        # Calculate new position
        angle_rad = math.radians(self.rotation[1])
        new_x = self.position[0] - math.sin(angle_rad) * self.speed
        new_z = self.position[2] - math.cos(angle_rad) * self.speed
        
        # Check if new position would be within bounds and not colliding with rectangle
        if self.environment:
            half_width = self.environment.width / 2
            half_depth = self.environment.depth / 2
            
            # Only update if within bounds and not colliding
            if (-half_width < new_x < half_width and 
                -half_depth < new_z < half_depth and
                not self.check_rectangle_collision(new_x, new_z)):
                self.position[0] = new_x
                self.position[2] = new_z
        
    def rotate_left(self):
        # Rotate counterclockwise around Y axis
        self.rotation[1] += self.rotation_speed
        if self.rotation[1] >= 360:
            self.rotation[1] -= 360
        
    def rotate_right(self):
        # Rotate clockwise around Y axis
        self.rotation[1] -= self.rotation_speed
        if self.rotation[1] < 0:
            self.rotation[1] += 360
        
    def draw(self):
        # Set color directly for solid color without lighting effects
        glDisable(GL_LIGHTING)
        glColor3f(*self.color)
        
        # Draw a simple triangular prism
        glBegin(GL_TRIANGLES)
        
        # Front triangle (pointing forward)
        glVertex3f(0, 0, self.size)         # Nose
        glVertex3f(-self.size/2, 0, -self.size)  # Left back
        glVertex3f(self.size/2, 0, -self.size)   # Right back
        
        # Top triangle
        glVertex3f(0, 0, self.size)         # Nose
        glVertex3f(0, self.size/2, -self.size)   # Top back
        glVertex3f(-self.size/2, 0, -self.size)  # Left back
        
        # Bottom triangle
        glVertex3f(0, 0, self.size)         # Nose
        glVertex3f(self.size/2, 0, -self.size)   # Right back
        glVertex3f(0, -self.size/2, -self.size)  # Bottom back
        glEnd()
        
        # Draw black outline
        glLineWidth(2.0)
        glColor3f(0.0, 0.0, 0.0)  # Black outline
        
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_TRIANGLES)
        
        # Front triangle outline
        glVertex3f(0, 0, self.size)         # Nose
        glVertex3f(-self.size/2, 0, -self.size)  # Left back
        glVertex3f(self.size/2, 0, -self.size)   # Right back
        
        # Top triangle outline
        glVertex3f(0, 0, self.size)         # Nose
        glVertex3f(0, self.size/2, -self.size)   # Top back
        glVertex3f(-self.size/2, 0, -self.size)  # Left back
        
        # Bottom triangle outline
        glVertex3f(0, 0, self.size)         # Nose
        glVertex3f(self.size/2, 0, -self.size)   # Right back
        glVertex3f(0, -self.size/2, -self.size)  # Bottom back
        glEnd()
        
        # Reset polygon mode and lighting
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glEnable(GL_LIGHTING)
