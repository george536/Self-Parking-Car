from carla_controls.abstract_command import CMD
import carla

class AttachCamera(CMD):
        def __init__(self, world, vehicle):
            self.world = world
            self.vehicle = vehicle
        
        def execute(self, img_height, img_width, fov,  location, rotation):
            # Attach a camera to the vehicle (we will use this to get the images from the perspective of the vehicle)
            camera_bp = self.world.get_blueprint_library().find('sensor.camera.rgb')
            camera_bp.set_attribute('image_size_x', str(img_width))
            camera_bp.set_attribute('image_size_y', str(img_height))
            camera_bp.set_attribute('fov', str(fov))
            camera_transform = carla.Transform(location.value, rotation.value)
            camera = self.world.spawn_actor(camera_bp, camera_transform, attach_to=self.vehicle)
            return camera