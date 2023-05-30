from connect_to_carla import ConnectToCarla
from add_vehicle import AddVehicle
from camera_locations import CameraLocations
from listen_to_image import process_image
from listen_to_image import perspective_transform
from attach_camera import AttachCamera
import threading
import threading

client = ConnectToCarla().execute()

world = client.get_world()

spectator = world.get_spectator()
spawn_point = spectator.get_transform()

vehicle = AddVehicle(world, spawn_point).execute()

camera1 = AttachCamera(world, vehicle).execute(480, 640, 90, CameraLocations.FrontLocation, CameraLocations.FrontRotation)

# Wait for all threads to finish
thread1.join()
thread2.join()
thread3.join()
thread4.join()

while True:
    world.tick()
