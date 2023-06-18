from Carla_Controls.connect_to_carla import ConnectToCarla
from Carla_Controls.add_vehicle import AddVehicle
from Birds_Eye_View.camera_locations import CameraLocations
from Carla_Controls.attach_camera import AttachCamera
from threading import Thread
from Birds_Eye_View.camera_configs_modifier import *
from Birds_Eye_View.camera_processing import generate_birds_eye_view
import pygame
from Birds_Eye_View.birds_eye_view_calibration import BEVCalibration

class BirdsEyeView(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        client = ConnectToCarla().execute()

        world = client.get_world()

        # Get all actors in the world
        actors = world.get_actors()

        # Destroy only car actors
        for actor in actors:
            if 'vehicle' in actor.type_id:
                actor.destroy()
        print("All Vehicle actors have been deleted")

        # Destroy all camera sensors
        for actor in actors:
            if'sensor.camera' in actor.type_id:
                actor.destroy()
        print("All Sensor cameras have been destroyed")

        spectator = world.get_spectator()
        spawn_point = spectator.get_transform()

        vehicle = AddVehicle(world, spawn_point).execute()

        # Carla Camera resolution
        h = 240
        w = 320

        config_modifications_insatnce = ConfigModifier.get_instance()
        pygame.init()
        window_size = (config_modifications_insatnce.pygame_window_dimensions['w'], config_modifications_insatnce.pygame_window_dimensions['h'])  # Set your desired window size
        window = pygame.display.set_mode(window_size)
        self.combined_surface = pygame.Surface(window_size, pygame.SRCALPHA)

        def camera_listen(id, camera):
            camera.listen(lambda image: generate_birds_eye_view(id, image, self.combined_surface))

        camera1 = AttachCamera(world, vehicle).execute(h, w, 150, CameraLocations.FrontLocation, CameraLocations.FrontRotation)
        camera2 = AttachCamera(world, vehicle).execute(h, w, 150, CameraLocations.RearLocation, CameraLocations.RearRotation)
        camera3 = AttachCamera(world, vehicle).execute(h, w, 90, CameraLocations.RightLocation, CameraLocations.RightRotation)
        camera4 = AttachCamera(world, vehicle).execute(h, w, 90, CameraLocations.LeftLocation, CameraLocations.LeftRotation)

        # Create threads for camera listens
        thread1 = Thread(target=camera_listen, args=(1, camera1))
        thread2 = Thread(target=camera_listen, args=(3, camera2))
        thread3 = Thread(target=camera_listen, args=(2, camera3))
        thread4 = Thread(target=camera_listen, args=(4, camera4))

        # Start the threads
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

        running = True
        while running:
            world.tick()
            window.blit(self.combined_surface, (0, 0))
            pygame.display.flip()

            # handle all events to avoid crashes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Bird's Eye view is being terminated..")
                    config_modifications_insatnce.save_camera_configs()
                    pygame.quit()
                    running = False
