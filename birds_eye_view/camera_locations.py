from enum import Enum
import carla

class CameraLocations(Enum):
    FrontLocation = carla.Location(x=2, y=0, z=2)
    FrontRotation = carla.Rotation(pitch=0, yaw=0, roll=0)

    RearLocation = carla.Location(x=-2, y=0, z=2)
    RearRotation = carla.Rotation(pitch=0, yaw=180, roll=0)

    RightLocation = carla.Location(x=1.2, y=0.5, z=2)
    RightRotation = carla.Rotation(pitch=0, yaw=90, roll=0)

    LeftLocation = carla.Location(x=1.2, y=-0.5, z=2)
    LeftRotation = carla.Rotation(pitch=0, yaw=270, roll=0)