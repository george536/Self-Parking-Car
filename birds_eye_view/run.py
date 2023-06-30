from carla_controls.connect_to_carla import ConnectToCarla
from carla_controls.add_vehicle import AddVehicle
from birds_eye_view.camera_locations import CameraLocations
from carla_controls.attach_camera import AttachCamera
from threading import Thread
from birds_eye_view.camera_configs_modifier import *
from birds_eye_view.camera_processing import generate_birds_eye_view
import pygame
from birds_eye_view.birds_eye_view_calibration import BEVCalibration
import carla
import time
from birds_eye_view.comb_surface_access import get_combined_surface, set_combined_surface, semaphore


class BirdsEyeView(Thread):
    
    def __init__(self, should_calibrate):
        super().__init__()
        self.should_calibrate = should_calibrate
        self.camera1 = None
        self.camera2 = None
        self.camera3 = None
        self.camera4 = None
        
        self.vehicle = None
        
        self.running = False
    

    def run(self):
        
        client = ConnectToCarla().execute()

        world = client.get_world()

        spectator = world.get_spectator()
        spawn_point = carla.Transform(carla.Location(x=-13.2, y=-27.2, z=2), carla.Rotation(pitch=0, yaw=180, roll=0))
        spectator.set_transform(spawn_point)
        self.vehicle = AddVehicle(world, spawn_point).execute()

        # Carla Camera resolution

        config_modifications_insatnce = ConfigModifier.get_instance()
        pygame.init()
        window_size = (config_modifications_insatnce.pygame_window_dimensions['w'], config_modifications_insatnce.pygame_window_dimensions['h'])  # Set your desired window size
        w = 1800
        h = 700
        window = pygame.display.set_mode(window_size)
        
        global combined_surface
        set_combined_surface(pygame.Surface(window_size, pygame.SRCALPHA))

        def camera_listen(id, camera):
            camera.listen(lambda image: generate_birds_eye_view(id, image))

        self.camera1 = AttachCamera(world, self.vehicle).execute(h, w, 150, CameraLocations.FrontLocation, CameraLocations.FrontRotation)
        self.camera2 = AttachCamera(world, self.vehicle).execute(h, w, 150, CameraLocations.RearLocation, CameraLocations.RearRotation)
        self.camera3 = AttachCamera(world, self.vehicle).execute(h, w, 150, CameraLocations.RightLocation, CameraLocations.RightRotation)
        self.camera4 = AttachCamera(world, self.vehicle).execute(h, w, 150, CameraLocations.LeftLocation, CameraLocations.LeftRotation)

        # Create threads for camera listens
        thread1 = Thread(target=camera_listen, args=(1, self.camera1)) ## front camera
        thread2 = Thread(target=camera_listen, args=(2, self.camera2)) ## rear camera
        thread3 = Thread(target=camera_listen, args=(3, self.camera3)) ## right camera
        thread4 = Thread(target=camera_listen, args=(4, self.camera4)) ## left camera

        # Start the threads
        if self.should_calibrate:
            biv_calibration = BEVCalibration()
            biv_calibration.start()
            
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
            window.blit(get_combined_surface(), (0, 0))
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
            config_modifications_insatnce.save_camera_configs()
            pygame.quit()
            self.vehicle.destroy()
            print("Vehicle has been destroyed.")
            self.camera1.destroy()
            self.camera2.destroy()
            self.camera3.destroy()
            self.camera4.destroy()
            print("Vehicle camera sensors have been destroyed.")