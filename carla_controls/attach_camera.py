<<<<<<< HEAD:carla_controls/attach_camera.py
from carla_controls.abstract_command import CMD
import carla

class AttachCamera(CMD):
=======
from utils.cmd import CMD
import carla

class AttachCameraToCar(CMD):
        
>>>>>>> f8f4313f3e927461ca78a93fa7043126918118ac:utils/attach_camera_car.py
        def __init__(self, world, vehicle):
            self.world = world
            self.vehicle = vehicle
        
        def execute(self, img_height, img_width, fov,  location, rotation):
            # Attach a camera to the vehicle (we will use this to get the images from the perspective of the vehicle)
            camera_bp = self.world.get_blueprint_library().find('sensor.camera.rgb')
            camera_bp.set_attribute('image_size_x', str(img_width))
            camera_bp.set_attribute('image_size_y', str(img_height))
            camera_bp.set_attribute('fov', str(fov))
            camera_bp.set_attribute('lens_k', '-1000.0')
            camera_bp.set_attribute('lens_kcube', '1000.0')
            camera_bp.set_attribute('lens_x_size', '1.0')
            camera_bp.set_attribute('lens_y_size', '1.0')
            camera_transform = carla.Transform(location.value, rotation.value)
            camera = self.world.spawn_actor(camera_bp, camera_transform, attach_to=self.vehicle)
            return camera