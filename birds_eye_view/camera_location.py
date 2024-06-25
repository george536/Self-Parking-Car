from enum import IntEnum
from carla import Location
from carla import Transform
from carla import Rotation

from birds_eye_view.camera_properties_calibration import CameraPropertiesCalibration

class CameraLocations(IntEnum):
    FRONT_LOCATION = 1
    REAR_LOCATION = 2
    RIGHT_LOCATION = 3
    LEFT_LOCATION = 4
    TOP_DOWN_LOCATION = 5

class CameraLocation:
    def __init__(self, location,
                 camera_location = Location(x=0, y=0, z=0),
                 camera_rotation = Rotation(pitch=0, yaw=0, roll=0), camera = None):
        self.location = location
        self.x = camera_location.x
        self.y = camera_location.y
        self.z = camera_location.z
        self.pitch = camera_rotation.pitch
        self.yaw = camera_rotation.yaw
        self.roll = camera_rotation.roll
        self.camera = camera
        CameraPropertiesCalibration.get_instance().add_camera(self)
        self.parse_json_fields(CameraPropertiesCalibration.get_instance().get_camera_locations_dictionary())

    def get_x(self):
        return self.x

    def set_x(self, value):
        self.x = value
        self.update_transform()

    def get_y(self):
        return self.y

    def set_y(self, value):
        self.y = value
        self.update_transform()

    def get_z(self):
        return self.z

    def set_z(self, value):
        self.z = value
        self.update_transform()

    def get_pitch(self):
        return self.pitch

    def set_pitch(self, value):
        self.pitch = value
        self.update_transform()

    def get_yaw(self):
        return self.yaw

    def set_yaw(self, value):
        self.yaw = value
        self.update_transform()

    def get_roll(self):
        return self.roll

    def set_roll(self, value):
        self.roll = value
        self.update_transform()

    def get_location(self):
        return Location(x = float(self.x), y = float(self.y), z = float(self.z))

    def get_rotation(self):
        return Rotation(pitch = float(self.pitch), yaw = float(self.yaw), roll = float(self.roll))

    def update_transform(self):
        self.camera.set_transform(Transform(self.get_location(), self.get_rotation()))

    def parse_json_fields(self,json_data):
        json_data = json_data[str(self.location.name)]
        self.x = float(json_data['x'])
        self.y = float(json_data['y'])
        self.z = float(json_data['z'])
        self.pitch = float(json_data['pitch'])
        self.yaw = float(json_data['yaw'])
        self.roll = float(json_data['roll'])
