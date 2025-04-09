import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from components.environment import Environment
from components.drone import Drone
from components.home_base import HomeBase
from components.flag import Flag

from utils.camera import Camera
from utils.mouse_handler import MouseHandler

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        pygame.display.set_mode((self.screen_width, self.screen_height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("3D Drone Environment")
        
        # Initialize the clock for frame rate control
        self.clock = pygame.time.Clock()
        
        # Create toggle button
        self.button_rect = pygame.Rect(10, self.screen_height - 40, 100, 30)  # x, y, width, height
        self.button_color = (100, 100, 100)  # Gray color
        self.button_hover = False
        
        self.setup_gl()
        
        # Create game objects
        self.environment = Environment(36, 10, 18)  # Adjusted container dimensions
        self.camera = Camera()
        self.camera.position = [0.0, 5.0, 30.0]  # Set initial camera position
        
        # Create game objects
        drone1 = Drone(color=(1.0, 0.0, 0.0), size=0.5)  # Red drone
        drone2 = Drone(color=(0.0, 0.0, 1.0), size=0.5)  # Blue drone
        base1 = HomeBase(color=(1.0, 0.0, 0.0), size=2)  # Red base
        base2 = HomeBase(color=(0.0, 0.0, 1.0), size=2)  # Blue base
        flag1 = Flag(color=(1.0, 0.0, 0.0), size=0.5)  # Red flag
        flag2 = Flag(color=(0.0, 0.0, 1.0), size=0.5)  # Blue flag
        
        # Set up all game objects in environment
        self.environment.set_game_objects(drone1, drone2, base1, base2, flag1, flag2)
        
        print("Environment created with dimensions:", self.environment.width, self.environment.height, self.environment.depth)
        print("Drone 1 position:", self.environment.drone1.position)
        print("Drone 2 position:", self.environment.drone2.position)
        
        self.last_time = pygame.time.get_ticks()

    def setup_gl(self):
        glClearColor(1.0, 1.0, 1.0, 1)  # White background
        
        # Set up perspective
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (800/600), 0.1, 100.0)
        
        # Enable depth testing and lighting
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
        # Set up light position and properties
        glLight(GL_LIGHT0, GL_POSITION, (5.0, 5.0, 5.0, 1.0))
        glLight(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1.0))
        glLight(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
        
        # Initialize ModelView matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        print("OpenGL setup completed")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEWHEEL:
                self.camera.handle_scroll(event.y)  # Trackpad/mouse wheel zoom
            elif event.type == pygame.KEYDOWN:
                self.camera.handle_key(event.unicode.encode())            # Handle mouse events for environment rotation
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
                # First check button interaction
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.button_rect.collidepoint(mouse_pos):
                        self.environment.rectangle.toggle()
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    self.button_hovered = self.button_rect.collidepoint(mouse_pos)
                
                # Then pass to environment for rotation
                self.environment.handle_mouse(event)
            
            # Only process key press/release events
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                pass  # We'll handle movement in the update loop
        return True

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()
            delta_time = (current_time - self.last_time) / 1000.0  # Convert to seconds
            self.last_time = current_time

            if not self.handle_events():
                pygame.quit()
                return

            # Update game state
            self.update()
            
            # Clear the screen and depth buffer
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # Reset the modelview matrix
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            
            # Apply camera transform
            self.camera.apply()
            
            # Draw the environment
            self.environment.draw()
            
            # Draw the 2D button on top
            self.draw_button()
            
            # Swap the display buffers
            pygame.display.flip()
            
            # Control the frame rate
            self.clock.tick(60)

    def update(self):
        # Get current keyboard state for continuous movement
        keys = pygame.key.get_pressed()
        
        # Drone 1 controls (WASD)
        if keys[pygame.K_w]:
            self.environment.drone1.move_forward()
        if keys[pygame.K_s]:
            self.environment.drone1.move_backward()
        if keys[pygame.K_a]:
            self.environment.drone1.rotate_left()
        if keys[pygame.K_d]:
            self.environment.drone1.rotate_right()
        
        # Drone 2 controls (Arrow keys)
        if keys[pygame.K_UP]:
            self.environment.drone2.move_forward()
        if keys[pygame.K_DOWN]:
            self.environment.drone2.move_backward()
        if keys[pygame.K_LEFT]:
            self.environment.drone2.rotate_left()
        if keys[pygame.K_RIGHT]:
            self.environment.drone2.rotate_right()

    def draw_button(self):
        # Save OpenGL state
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.screen_width, self.screen_height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Disable everything that could interfere with 2D rendering
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        
        # Draw button background
        button_color = (150, 150, 150) if self.button_hover else (100, 100, 100)
        
        # Convert button rect to raw OpenGL commands for guaranteed visibility
        glBegin(GL_QUADS)
        glColor3f(button_color[0]/255.0, button_color[1]/255.0, button_color[2]/255.0)
        glVertex2f(self.button_rect.left, self.button_rect.top)
        glVertex2f(self.button_rect.right, self.button_rect.top)
        glVertex2f(self.button_rect.right, self.button_rect.bottom)
        glVertex2f(self.button_rect.left, self.button_rect.bottom)
        glEnd()
        
        # Draw button outline
        glColor3f(0, 0, 0)  # Black
        glBegin(GL_LINE_LOOP)
        glVertex2f(self.button_rect.left, self.button_rect.top)
        glVertex2f(self.button_rect.right, self.button_rect.top)
        glVertex2f(self.button_rect.right, self.button_rect.bottom)
        glVertex2f(self.button_rect.left, self.button_rect.bottom)
        glEnd()
        
        # Draw text using pygame's surface
        font = pygame.font.Font(None, 24)
        text = font.render('Toggle', True, (255, 255, 255))
        text_rect = text.get_rect(center=self.button_rect.center)
        pygame.display.get_surface().blit(text, text_rect)
        
        # Restore OpenGL state
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glPopAttrib()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
