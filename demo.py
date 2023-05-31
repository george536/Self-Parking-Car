from utils.connect_to_carla import ConnectToCarla
from utils.add_vehicle import AddVehicle
from utils.camera_locations import CameraLocations
from utils.listen_to_image import process_image
from utils.listen_to_image import perspective_transform
from utils.attach_camera import AttachCameraToCar


client = ConnectToCarla().execute()

world = client.get_world()

spectator = world.get_spectator()
spawn_point = spectator.get_transform()

vehicle = AddVehicle(world, spawn_point).execute()

camera1 = AttachCameraToCar(world, vehicle).execute(480, 640, 90, CameraLocations.FrontLocation, CameraLocations.FrontRotation)

camera1.listen(lambda image: perspective_transform(image, 480, 640))

while True:
    world.tick()
