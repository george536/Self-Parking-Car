from enum import IntEnum
import carla

from birds_eye_view.camera_properties_calibration import CameraPropertiesCalibration

class CameraLocations(IntEnum):
    FrontLocation = 1
    RearLocation = 2
    RightLocation = 3
    LeftLocation = 4

class CameraLocation:
    def __init__(self, location, 
                 camera_location = carla.Location(x=0, y=0, z=0),
                 camera_rotation = carla.Rotation(pitch=0, yaw=0, roll=0), camera = None):
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
        return carla.Location(x = self.x, y = self.y, z = self.z)
    
    def get_rotation(self):
        return carla.Rotation(pitch = self.pitch, yaw = self.yaw, roll = self.roll)

    def update_transform(self):
        self.camera.set_transform(carla.Transform(self.get_location(), self.get_rotation()))

    def parse_json_fields(self,jsonData):
        jsonData = jsonData[str(self.location.name)]
        self.x = jsonData['x']
        self.y = jsonData['y']
        self.z = jsonData['z']
        self.pitch = jsonData['pitch']
        self.yaw = jsonData['yaw']
        self.roll = jsonData['roll']