from threading import Thread
import time
import pygame
from carla import Transform
from carla import Rotation
from carla import Location
import numpy as np

from carla_controls.connect_to_carla import ConnectToCarla
from carla_controls.attach_camera import AttachCamera
from carla_controls.add_vehicle import AddVehicle
from birds_eye_view.camera_location import CameraLocation
from birds_eye_view.camera_location import CameraLocations
from birds_eye_view.camera_configs_modifier import ConfigModifier
from birds_eye_view.camera_processing import *
from birds_eye_view.birds_eye_view_calibration import BEVCalibration
from birds_eye_view.comb_surface_access import *
from birds_eye_view.camera_properties_calibration import CameraPropertiesCalibration
from birds_eye_view.BEV_field_labeller import BEVFieldLabeller
from parking_spot_labeller.utils_labeller import load_parking_spots
from python_ipc.IpcClient import IpcClient

class BirdsEyeView(Thread):
    """Generates bird's eye view of the vehicle"""
    def __init__(self, should_calibrate, ipc_on, should_load_spots, should_show_bev_filed_box):
        super().__init__()
        self.should_calibrate = should_calibrate
        self.ipc_on = ipc_on
        self.camera1 = None
        self.camera2 = None
        self.camera3 = None
        self.camera4 = None
        self.top_down_camera = None
        self.vehicle = None

        self.running = False
        self.should_load_spots = should_load_spots
        self.should_show_bev_filed_box = should_show_bev_filed_box

        self.BEV_field_labeller = None

    def run(self):
        client = ConnectToCarla().execute()

        world = client.get_world()
        if self.should_load_spots:
            load_parking_spots(world)

        spectator = world.get_spectator()
        spawn_point = Transform(Location(x=-13.2, y=-27.2, z=0.2), Rotation(pitch=0, yaw=-78, roll=0))
        spectator.set_transform(spawn_point)
        self.vehicle = AddVehicle(world, spawn_point).execute()

        self.BEV_field_labeller = BEVFieldLabeller(world, self.vehicle, self.should_show_bev_filed_box)

        # Carla Camera resolution
        config_modifications_insatnce = ConfigModifier.get_instance()
        pygame.init()
        window_size = (config_modifications_insatnce.pygame_window_dimensions['w'],
                       config_modifications_insatnce.pygame_window_dimensions['h'])
        w = 640
        h = 480
        window = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Bird's eye view")

        global combined_surface
        set_combined_surface(pygame.Surface(window_size, pygame.SRCALPHA))

        if (self.ipc_on):
            top_down_camera_location = CameraLocation(CameraLocations.TOP_DOWN_LOCATION)

            self.top_down_camera = AttachCamera(world, self.vehicle).execute(
                h, w, 100, top_down_camera_location.get_location(), top_down_camera_location.get_rotation())
            top_down_camera_location.camera = self.top_down_camera

            self.top_down_camera.listen(lambda image: generate_top_down_view(5, image))
        else:
            camera_location1 = CameraLocation(CameraLocations.FRONT_LOCATION)
            camera_location2 = CameraLocation(CameraLocations.REAR_LOCATION)
            camera_location3 = CameraLocation(CameraLocations.RIGHT_LOCATION)
            camera_location4 = CameraLocation(CameraLocations.LEFT_LOCATION)

            self.camera1 = AttachCamera(world, self.vehicle).execute(
                h, w, 150, camera_location1.get_location(), camera_location1.get_rotation())
            self.camera2 = AttachCamera(world, self.vehicle).execute(
                h, w, 150, camera_location2.get_location(), camera_location2.get_rotation())
            self.camera3 = AttachCamera(world, self.vehicle).execute(
                h, w, 170, camera_location3.get_location(), camera_location3.get_rotation())
            self.camera4 = AttachCamera(world, self.vehicle).execute(
                h, w, 170, camera_location4.get_location(), camera_location4.get_rotation())

            camera_location1.camera = self.camera1
            camera_location2.camera = self.camera2
            camera_location3.camera = self.camera3
            camera_location4.camera = self.camera4

            combine_images_thread = Thread(target=combine_images, args=())
            combine_images_thread.start()
            
            self.camera1.listen(lambda image: generate_birds_eye_view(1, image))
            self.camera2.listen(lambda image: generate_birds_eye_view(2, image))
            self.camera3.listen(lambda image: generate_birds_eye_view(3, image))
            self.camera4.listen(lambda image: generate_birds_eye_view(4, image))

        if self.should_calibrate:
            biv_calibration = BEVCalibration()
            biv_calibration.start()
            CameraPropertiesCalibration.get_instance().start()
            
        self.running = True
        while self.running:
            world.tick()
            combined_surface_semaphore.acquire()
            combined_surface = get_combined_surface()
            window.blit(combined_surface, (0, 0))
            self.BEV_field_labeller.update_box()
            
            if self.ipc_on:
                self.process_ipc_actions()

            combined_surface_semaphore.release()
            pygame.display.flip()

            # handle all events to avoid crashes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.at_exit()
                    self.running = False

            time.sleep(0.01)

    def process_ipc_actions(self):
        """Sends image data and transform data over to the ipc server"""
        # Convert Pygame Surface to bytes array to be sent over ipc if needed
        IpcClient.semaphore1.acquire()
        surface_bytes = pygame.image.tostring(combined_surface, 'RGB')
        rgb_data = np.frombuffer(surface_bytes, dtype=np.uint8)
        IpcClient.get_instance().set_image_data(rgb_data)
        IpcClient.get_instance().set_transform_data(self.vehicle.get_transform())
        IpcClient.get_instance().set_BEV_bounding_box_cord(self.BEV_field_labeller.get_field_box_points())
        IpcClient.semaphore2.release()

    def at_exit(self):
        """Actions performed at program exit"""
        if self.running is True:
            config_modifications_insatnce = ConfigModifier.get_instance()
            print("Bird's Eye view is being terminated..")
            if self.should_calibrate:
                config_modifications_insatnce.save_camera_configs()
                CameraPropertiesCalibration.get_instance().save_camera_properties()
            pygame.quit()
            self.vehicle.destroy()
            print("Vehicle has been destroyed.")
            self.camera1.destroy()
            self.camera2.destroy()
            self.camera3.destroy()
            self.camera4.destroy()
            print("Vehicle camera sensors have been destroyed.")
