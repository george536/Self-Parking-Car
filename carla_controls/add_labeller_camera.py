import numpy as np
import pygame
import carla

from carla_controls.abstract_command import CMD

class LabellerCamera(CMD):
  """Camera object to have a surface."""
  def __init__(self,world, camera_type="rgb", image_type=carla.ColorConverter.Raw,
               width=None, height=None, fov=None):
    
    self.image_type = image_type
    self.world = world
    self.width = width
    self.height = height
    self.fov = fov
    self.camera_type = camera_type

  def execute(self):

    self.camera_actor = self.create_camera()
    
    self.rgb_image = None  # last RGB image
    self.pygame_surface = None  # last RGB image made pygame surface

    # initialize
    self.camera_actor.listen(self.parse_image)
    if self.camera_type == "rgb":
      self.camera_actor.intrinsic = self.compute_intrinsic()

    return self

  # callback for sensor.listen()
  # this is called whenever a data comes from CARLA server
  def parse_image(self, image):
    """Process one camera captured image."""
    # parse the image data into a pygame surface for display or screenshot
    # raw image is BGRA
    # if image_type is segmentation, here will convert to the pre-defined color
    image.convert(self.image_type)

    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]  # BGR -> RGB
    self.rgb_image = array
    self.pygame_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
    
  def compute_intrinsic(self):
    """Compute intrinsic matrix."""
    intrinsic = np.identity(3)
    intrinsic[0, 2] = self.width / 2.0
    intrinsic[1, 2] = self.height / 2.0
    intrinsic[0, 0] = intrinsic[1, 1] = self.width / (2.0 * np.tan(self.fov *
                                                                  np.pi / 360.0))
    return intrinsic
  
  def create_camera(self):
    bp_id = 'sensor.camera.rgb' if self.camera_type == "rgb" else 'sensor.camera.depth'
    camera_bp = self.world.get_blueprint_library().find(bp_id)
    camera_bp.set_attribute('image_size_x', '%s' % self.width)
    camera_bp.set_attribute('image_size_y', '%s' % self.height)
    camera_bp.set_attribute('fov', '%s' % self.fov)
    camera_bp.set_attribute("sensor_tick", "%s" % 0.0)
    camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
    camera = self.world.spawn_actor(camera_bp, camera_transform, self.world.get_spectator())

    return camera