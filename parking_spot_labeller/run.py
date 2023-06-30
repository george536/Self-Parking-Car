import numpy as np
import carla
import pygame

from carla_controls.connect_to_carla import ConnectToCarla
from carla_controls.add_labeller_camera import LabellerCamera
from parking_spot_labeller.utils_labeller import get_3d_points

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FOV = 110

class parking_labeller:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([1280, 720])
        self.running = True
        self.client = ConnectToCarla().execute()
        
        self.world = self.client.get_world()
        self.camera = LabellerCamera(self.world, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fov=FOV, camera_type="rgb").execute()
        self.depth_camera = LabellerCamera(self.world, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fov=FOV, camera_type="depth").execute()
        self.draw_debug_points = []
        
    
    def destroy_cameras(self):
        self.camera.camera_actor.destroy()
        self.depth_camera.camera_actor.destroy()
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONUP:
                    self.draw_debug_points.append(get_3d_points(self.camera, self.depth_camera))
                    self.world.debug.draw_point(carla.Location(x=self.draw_debug_points[-1][0], y=self.draw_debug_points[-1][1], z=self.draw_debug_points[-1][2]), size=0.1, life_time=1000)
                if event.type == pygame.QUIT:
                    self.running = False
             
            if self.camera.pygame_surface is not None:
                self.screen.blit(self.camera.pygame_surface, (0, 0))
            else:
                self.screen.fill([255, 255, 255])
            
            pygame.display.flip()
    
        self.destroy_cameras()
        pygame.quit()
