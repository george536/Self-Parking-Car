from enum import Enum
import carla

class CameraLocations(Enum):
    FrontLocation = carla.Location(x=2.6, y=0, z=1)
    FrontRotation = carla.Rotation(pitch=-20, yaw=0, roll=0)

    RearLocation = carla.Location(x=-2.7, y=0, z=1.5)
    RearRotation = carla.Rotation(pitch=-40, yaw=180, roll=0)

    RightLocation = carla.Location(x=0.9, y=2.7, z=1)
    RightRotation = carla.Rotation(pitch=-90, yaw=90, roll=0)

    LeftLocation = carla.Location(x=0.9, y=-2.7, z=1)
    LeftRotation = carla.Rotation(pitch=-90, yaw=-90, roll=0)