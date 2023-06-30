from enum import Enum
import carla

class CameraLocations(Enum):
    FrontLocation = carla.Location(x=2.2, y=0, z=1.7)
    FrontRotation = carla.Rotation(pitch=0, yaw=0, roll=0)

    RearLocation = carla.Location(x=-2.2, y=0, z=1.7)
    RearRotation = carla.Rotation(pitch=-15, yaw=180, roll=0)

    RightLocation = carla.Location(x=1.2, y=1.2, z=1.5)
    RightRotation = carla.Rotation(pitch=60, yaw=0, roll=0)

    LeftLocation = carla.Location(x=1.2, y=-1.2, z=1.5)
    LeftRotation = carla.Rotation(pitch=60, yaw=0, roll=0)