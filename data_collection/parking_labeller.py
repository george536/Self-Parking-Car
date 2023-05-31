import pygame
from utils.connect_to_carla import ConnectToCarla
from data_collection.camera_world import Camera
import carla
from data_collection.utils_labeller import get_3d_points

import numpy as np

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FOV = 110

class parking_labeller:
    
    def __init__(self, load_world=None):
        pygame.init()
        self.screen = pygame.display.set_mode([1280, 720])
        self.running = True
        self.client = ConnectToCarla().execute()
        
        if load_world is not None:
            self.world = self.client.load_world(load_world)
        
        self.world = self.client.get_world()
        self.camera = Camera(self.world, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fov=FOV, camera_type="rgb")
        self.depth_camera = Camera(self.world, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fov=FOV, camera_type="depth")
        self.draw_debug_points = []
        
    
    def destroy_cameras(self):
        self.camera.camera_actor.destroy()
        self.depth_camera.camera_actor.destroy()
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONUP:
                    self.draw_debug_points.append(get_3d_points(self.camera, self.depth_camera))
                    print(self.draw_debug_points[-1])
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
