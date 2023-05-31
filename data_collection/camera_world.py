import numpy as np
from data_collection.utils_labeller import compute_intrinsic
import pygame
import carla

class Camera(object):
  """Camera object to have a surface."""
  def __init__(self, camera_actor, camera_type="rgb", image_type=carla.ColorConverter.Raw,
               width=None, height=None, fov=None, recording=False):
    self.camera_actor = camera_actor
    self.image_type = image_type

    self.last_image_frame_num = None  # the frame num of the image
    self.last_image_seconds = None  # the seconds since beginning of eposide?
    self.rgb_image = None  # last RGB image
    self.pygame_surface = None  # last RGB image made pygame surface

    self.camera_type = camera_type

    # initialize
    camera_actor.listen(self.parse_image)
    if self.camera_type == "rgb":
      self.camera_actor.intrinsic = compute_intrinsic(width, height, fov)

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