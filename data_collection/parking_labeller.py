import pygame
from utils.connect_to_carla import ConnectToCarla
from data_collection.camera_world import Camera
import carla
from data_collection.utils_labeller import parse_carla_depth
from data_collection.utils_labeller import compute_extrinsic_from_transform

import numpy as np

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
        camera_actor, depth_camera_actor = self.create_cameras()
        self.camera = Camera(camera_actor, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fov=FOV, camera_type="rgb")
        self.depth_camera = Camera(depth_camera_actor, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fov=FOV, camera_type="depth")
        self.draw_debug_points = []
    
    
    def create_cameras(self):
        camera_bp = self.world.get_blueprint_library().find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', '%s' % WINDOW_WIDTH)
        camera_bp.set_attribute('image_size_y', '%s' % WINDOW_HEIGHT)
        camera_bp.set_attribute('fov', '%s' % FOV)
        camera_bp.set_attribute("sensor_tick", "%s" % 0.0)
        camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        camera = self.world.spawn_actor(camera_bp, camera_transform, self.world.get_spectator())
        
        camera_depth_bp = self.world.get_blueprint_library().find("sensor.camera.depth")
        camera_depth_bp.set_attribute("image_size_x", "%s" % WINDOW_WIDTH)
        camera_depth_bp.set_attribute("image_size_y", "%s" % WINDOW_HEIGHT)
        camera_depth_bp.set_attribute("fov", "%s" % FOV)
        camera_depth_bp.set_attribute("sensor_tick", "%s" % 0.0)
        
        camera_depth = self.world.spawn_actor(camera_depth_bp, camera_transform, self.world.get_spectator())
        return camera, camera_depth
    
    def get_3d_points(self):
        depth_in_meters = parse_carla_depth(self.depth_camera.rgb_image)
        pos_x, pos_y = pygame.mouse.get_pos()
        click_point = np.array([pos_x, pos_y, 1])
        intrinsic = self.camera.camera_actor.intrinsic
        
        click_point_3d = np.dot(np.linalg.inv(intrinsic), click_point)
        click_point_3d *= depth_in_meters[pos_y, pos_x]
        
        y,z,x = click_point_3d
        z = -z
        
        click_point_3d = np.array([x,y,z, 1])
        click_point_3d.reshape((4,1))
        
        camera_rt = compute_extrinsic_from_transform(self.camera.camera_actor.get_transform())
        
        click_point_world_3d = np.dot(camera_rt, click_point_3d)
        
        return click_point_world_3d.tolist()[0][:3]
        
        
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONUP:
                    self.draw_debug_points.append(self.get_3d_points())
                    print(self.draw_debug_points[-1])
                    self.world.debug.draw_point(carla.Location(x=self.draw_debug_points[-1][0], y=self.draw_debug_points[-1][1], z=self.draw_debug_points[-1][2]), size=0.1, life_time=1000)
                if event.type == pygame.QUIT:
                    self.running = False
             
            if self.camera.pygame_surface is not None:
                self.screen.blit(self.camera.pygame_surface, (0, 0))
            else:
                self.screen.fill([255, 255, 255])
            
            pygame.display.flip()
            
        pygame.quit()
