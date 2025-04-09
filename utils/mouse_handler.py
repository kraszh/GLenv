import pygame

class MouseHandler:
    def __init__(self):
        self.last_mouse_pos = None
        self.zoom = -15
        self.total_rotation_x = 0
        self.total_rotation_y = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.last_mouse_pos = pygame.mouse.get_pos()
            elif event.button == 4:  # Mouse wheel up
                self.zoom += 1  # Zoom in
            elif event.button == 5:  # Mouse wheel down
                self.zoom -= 1  # Zoom out
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click release
                self.last_mouse_pos = None
                
        elif event.type == pygame.MOUSEMOTION:
            if self.last_mouse_pos is not None:  # If dragging
                current_pos = pygame.mouse.get_pos()
                delta_x = current_pos[0] - self.last_mouse_pos[0]
                delta_y = current_pos[1] - self.last_mouse_pos[1]
                
                # Update cumulative rotation
                self.total_rotation_y += delta_x * 0.5
                self.total_rotation_x += delta_y * 0.5
                
                self.last_mouse_pos = current_pos
        
        # Clamp zoom level
        self.zoom = max(-30, min(-5, self.zoom))
