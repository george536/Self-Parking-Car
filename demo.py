from connect_to_carla import ConnectToCarla
from add_vehicle import AddVehicle
from camera_locations import CameraLocations
from listen_to_image import process_image
from listen_to_image import perspective_transform
from attach_camera import AttachCamera
import threading

client = ConnectToCarla().execute()

world = client.get_world()

spectator = world.get_spectator()
spawn_point = spectator.get_transform()

vehicle = AddVehicle(world, spawn_point).execute()

w = 320
h = 240

def camera_listen(id, camera, h, w, offset):
    camera.listen(lambda image: perspective_transform(id, image, h, w, offset))

camera1 = AttachCamera(world, vehicle).execute(h, w, 90, CameraLocations.FrontLocation, CameraLocations.FrontRotation)
camera2 = AttachCamera(world, vehicle).execute(h, w, 90, CameraLocations.RearLocation, CameraLocations.RearRotation)
camera3 = AttachCamera(world, vehicle).execute(h, w, 140, CameraLocations.RightLocation, CameraLocations.RightRotation)
camera4 = AttachCamera(world, vehicle).execute(h, w, 140, CameraLocations.LeftLocation, CameraLocations.LeftRotation)

# Create threads for camera listens
thread1 = threading.Thread(target=camera_listen, args=(1, camera1, h, w, 50))
thread2 = threading.Thread(target=camera_listen, args=(3, camera2, h, w, 50))
thread3 = threading.Thread(target=camera_listen, args=(2, camera3, h, w, 70))
thread4 = threading.Thread(target=camera_listen, args=(4, camera4, h, w, 70))

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
