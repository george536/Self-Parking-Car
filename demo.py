from connect_to_carla import ConnectToCarla
from add_vehicle import AddVehicle
from camera_locations import CameraLocations
from listen_to_image import process_image
from listen_to_image import perspective_transform
from attach_camera import AttachCamera
import threading
from camera_config import *
from camera_processing import generate_birds_eye_view

import pygame

client = ConnectToCarla().execute()

world = client.get_world()

spectator = world.get_spectator()
spawn_point = spectator.get_transform()

vehicle = AddVehicle(world, spawn_point).execute()

h = 240
w = 320

pygame.init()
window_size = (pygame_window_dimensions['w'], pygame_window_dimensions['h'])  # Set your desired window size
window = pygame.display.set_mode(window_size)
combined_surface = pygame.Surface(window_size, pygame.SRCALPHA)

def camera_listen(id, camera):
    global combined_surface
    camera.listen(lambda image: generate_birds_eye_view(id, image, combined_surface))

camera1 = AttachCamera(world, vehicle).execute(h, w, 90, CameraLocations.FrontLocation, CameraLocations.FrontRotation)
camera2 = AttachCamera(world, vehicle).execute(h, w, 90, CameraLocations.RearLocation, CameraLocations.RearRotation)
camera3 = AttachCamera(world, vehicle).execute(h, w, 90, CameraLocations.RightLocation, CameraLocations.RightRotation)
camera4 = AttachCamera(world, vehicle).execute(h, w, 90, CameraLocations.LeftLocation, CameraLocations.LeftRotation)

# Create threads for camera listens
thread1 = threading.Thread(target=camera_listen, args=(1, camera1))
thread2 = threading.Thread(target=camera_listen, args=(3, camera2))
thread3 = threading.Thread(target=camera_listen, args=(2, camera3))
thread4 = threading.Thread(target=camera_listen, args=(4, camera4))

# Start the threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()

# Wait for all threads to finish
thread1.join()
thread2.join()
thread3.join()
thread4.join()

while True:
    world.tick()
    window.blit(combined_surface, (0, 0))
    pygame.display.flip()
