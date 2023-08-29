from threading import Thread
import pygame
import carla
import time
import tkinter as tk
import cv2
import numpy as np

from carla_controls.connect_to_carla import ConnectToCarla
from carla_controls.add_vehicle import AddVehicle
from birds_eye_view.camera_location import CameraLocation
from birds_eye_view.camera_location import CameraLocations
from carla_controls.attach_camera import AttachCamera
from birds_eye_view.camera_configs_modifier import *
from birds_eye_view.camera_processing import generate_birds_eye_view
from birds_eye_view.birds_eye_view_calibration import BEVCalibration
from birds_eye_view.comb_surface_access import get_combined_surface, set_combined_surface, semaphore
from parking_spot_labeller.utils_labeller import load_parking_spots
from birds_eye_view.camera_properties_calibration import CameraPropertiesCalibration
from python_IPC.IPC_client import IPC_client

class BirdsEyeView(Thread):
    
    def __init__(self, should_calibrate, ipc_on):
        super().__init__()
        self.should_calibrate = should_calibrate
        self.ipc_on = ipc_on
        self.camera1 = None
        self.camera2 = None
        self.camera3 = None
        self.camera4 = None
        
        self.vehicle = None
        
        self.running = False

    def run(self):
        
        client = ConnectToCarla().execute()

        world = client.get_world()
        load_parking_spots(world)

        spectator = world.get_spectator()
        spawn_point = carla.Transform(carla.Location(x=-13.2, y=-27.2, z=2), carla.Rotation(pitch=0, yaw=-78, roll=0))
        spectator.set_transform(spawn_point)
        self.vehicle = AddVehicle(world, spawn_point).execute()

        # Carla Camera resolution

        config_modifications_insatnce = ConfigModifier.get_instance()
        pygame.init()
        window_size = (config_modifications_insatnce.pygame_window_dimensions['w'], config_modifications_insatnce.pygame_window_dimensions['h'])  # Set your desired window size
        w = 640
        h = 480
        window = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Bird's eye view")
        
        global combined_surface
        set_combined_surface(pygame.Surface(window_size, pygame.SRCALPHA))

        def camera_listen(id, camera):
            camera.listen(lambda image: generate_birds_eye_view(id, image))

        camera_location1 = CameraLocation(CameraLocations.FrontLocation)
        camera_location2 = CameraLocation(CameraLocations.RearLocation)
        camera_location3 = CameraLocation(CameraLocations.RightLocation)
        camera_location4 = CameraLocation(CameraLocations.LeftLocation)

        self.camera1 = AttachCamera(world, self.vehicle).execute(h, w, 150, camera_location1.get_location(), camera_location1.get_rotation())
        self.camera2 = AttachCamera(world, self.vehicle).execute(h, w, 150, camera_location2.get_location(), camera_location2.get_rotation())
        self.camera3 = AttachCamera(world, self.vehicle).execute(h, w, 170, camera_location3.get_location(), camera_location3.get_rotation())
        self.camera4 = AttachCamera(world, self.vehicle).execute(h, w, 170, camera_location4.get_location(), camera_location4.get_rotation())

        camera_location1.camera = self.camera1
        camera_location2.camera = self.camera2
        camera_location3.camera = self.camera3
        camera_location4.camera = self.camera4
        # Create threads for camera listens
        thread1 = Thread(target=camera_listen, args=(1, self.camera1)) ## front camera
        thread2 = Thread(target=camera_listen, args=(2, self.camera2)) ## rear camera
        thread3 = Thread(target=camera_listen, args=(3, self.camera3)) ## right camera
        thread4 = Thread(target=camera_listen, args=(4, self.camera4)) ## left camera

        # Start the threads
        if self.should_calibrate:
            biv_calibration = BEVCalibration()
            biv_calibration.start()
            CameraPropertiesCalibration.get_instance().start()
            
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()

        # Wait for all threads to finish
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()

        self.running = True
        
        while self.running:
            world.tick()
            semaphore.acquire()
            combined_surface = get_combined_surface()
            window.blit(combined_surface, (0, 0))
            if self.ipc_on:
                # Convert Pygame Surface to bytes array to be sent over ipc if needed
                IPC_client.semaphore1.acquire()
                surface_bytes = pygame.image.tostring(combined_surface, 'RGB')
                rgb_data = np.frombuffer(surface_bytes, dtype=np.uint8)
                rgb_image = rgb_data.reshape((450, 295, 3))

                # Convert RGB image to BGR (OpenCV's default format)
                bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

                # Display the image using cv2.imshow()
                cv2.imshow('RGB Image', bgr_image)
                IPC_client.get_instance().set_image_data(rgb_data)
                IPC_client.get_instance().set_transform(self.vehicle.get_transform())
                IPC_client.semaphore2.release()

            semaphore.release()
            pygame.display.flip()

            # handle all events to avoid crashes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.at_exit()
                    self.running = False
                    
            time.sleep(0.01)
                    

    def at_exit(self):
        if self.running == True:    
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