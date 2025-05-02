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
        self.captured_flag = None  # Reference to the captured flag
        self.is_blue = color[2] > color[0]  # True if drone is blue, False if red
        
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
                
    def check_divider_wall_collision(self, new_x):
        if not self.environment or not self.captured_flag:
            return False
            
        # Get wall position and dimensions
        wall = self.environment.divider_wall
        wall_x = wall.position[0]
        wall_thickness = wall.thickness
        
        # Add a small buffer around the wall
        buffer = 0.2
        
        # Check if drone would cross the wall
        current_x = self.position[0]
        if (current_x < wall_x and new_x > wall_x) or (current_x > wall_x and new_x < wall_x):
            # If crossing and carrying flag, trigger reset
            self.environment.reset_game()
            return True
            
        return False
        
    def check_drone_collision(self, new_x, new_y, new_z):
        if not self.environment:
            return False
            
        # Get the other drone
        other_drone = self.environment.drone2 if self == self.environment.drone1 else self.environment.drone1
        
        # Calculate distance between drones
        dx = new_x - other_drone.position[0]
        dy = new_y - other_drone.position[1]
        dz = new_z - other_drone.position[2]
        
        # Check if within collision radius (increased for better detection)
        collision_radius = 2.0  # Increased from 1.0 to 2.0
        distance_squared = dx * dx + dy * dy + dz * dz
        if distance_squared <= collision_radius * collision_radius:
            # If other drone has a flag, return it to base
            if other_drone.captured_flag:
                # Reset flag to its home position
                other_drone.captured_flag.reset_position()
                other_drone.captured_flag = None
            return True
            
        return False
                
    def check_flag_collision(self, flag):
        # Don't check if we already have a flag or if it's the same color as the drone
        if self.captured_flag or \
           (self.is_blue and flag.color[2] > flag.color[0]) or \
           (not self.is_blue and flag.color[0] > flag.color[2]):
            return False
            
        # Calculate distance between drone's nose and flag
        angle_rad = math.radians(self.rotation[1])
        nose_x = self.position[0] + math.sin(angle_rad) * self.size
        nose_z = self.position[2] + math.cos(angle_rad) * self.size
        
        dx = nose_x - flag.position[0]
        dy = self.position[1] - flag.position[1]
        dz = nose_z - flag.position[2]
        
        # Check if within capture radius
        capture_radius = 3.0  # Increased from 1.0 to make capture easier
        return (dx * dx + dy * dy + dz * dz) <= capture_radius * capture_radius
        
    def update_captured_flag_position(self):
        if self.captured_flag:
            # Update flag position relative to drone's nose
            angle_rad = math.radians(self.rotation[1])
            offset = 1.0  # Distance in front of drone
            
            # Calculate position in front of drone
            self.captured_flag.position[0] = self.position[0] + math.sin(angle_rad) * offset
            self.captured_flag.position[1] = self.position[1]  # Same height as drone
            self.captured_flag.position[2] = self.position[2] + math.cos(angle_rad) * offset
            
            # Check for collision with other drone
            other_drone = self.environment.drone2 if self == self.environment.drone1 else self.environment.drone1
            dx = self.captured_flag.position[0] - other_drone.position[0]
            dy = self.captured_flag.position[1] - other_drone.position[1]
            dz = self.captured_flag.position[2] - other_drone.position[2]
            
            # If flag collides with other drone, reset it
            collision_radius = 2.0
            if (dx * dx + dy * dy + dz * dz) <= collision_radius * collision_radius:
                self.captured_flag.reset_position()
                self.captured_flag = None
                
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
                # Check for divider wall and drone collisions first
                if not self.check_divider_wall_collision(new_x) and \
                   not self.check_drone_collision(new_x, self.position[1], new_z):
                    self.position[0] = new_x
                    self.position[2] = new_z
                    
                    # Check for flag collision
                    if not self.captured_flag:
                        for flag in [self.environment.flag1, self.environment.flag2]:
                            if self.check_flag_collision(flag):
                                self.captured_flag = flag
                                break
                                
                    # Update captured flag position
                    self.update_captured_flag_position()
        
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
                # Check for divider wall and drone collisions first
                if not self.check_divider_wall_collision(new_x) and \
                   not self.check_drone_collision(new_x, self.position[1], new_z):
                    self.position[0] = new_x
                    self.position[2] = new_z
                    
                    # Check for flag collision
                    if not self.captured_flag:
                        for flag in [self.environment.flag1, self.environment.flag2]:
                            if self.check_flag_collision(flag):
                                self.captured_flag = flag
                                break
                                
                    # Update captured flag position
                    self.update_captured_flag_position()

    def move_upward(self):
        # calculate new position
        new_y = self.position[1] + self.speed
        
        if self.environment:
            half_height = self.environment.height / 2
            
            # Only update if within bounds and not colliding
            if (-half_height < new_y < half_height and 
                not self.check_rectangle_collision(self.position[0], new_y)):
                self.position[1] = new_y
                self.update_captured_flag_position()

    def move_downward(self):
        # calculate new position
        new_y = self.position[1] - self.speed
        
        if self.environment:
            half_height = self.environment.height / 2
            
            # Only update if within bounds and not colliding
            if (-half_height < new_y < half_height and 
                not self.check_rectangle_collision(self.position[0], new_y)):
                self.position[1] = new_y
                self.update_captured_flag_position()
   
    def rotate_left(self):
        # Rotate counterclockwise around Y axis
        self.rotation[1] += self.rotation_speed
        if self.rotation[1] >= 360:
            self.rotation[1] -= 360
        self.update_captured_flag_position()
        
    def rotate_right(self):
        # Rotate clockwise around Y axis
        self.rotation[1] -= self.rotation_speed
        if self.rotation[1] < 0:
            self.rotation[1] += 360
        self.update_captured_flag_position()
        
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
