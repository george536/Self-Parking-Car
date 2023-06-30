
import pygame

import carla

import numpy as np

def get_3d_points(camera, depth_camera):
        depth_in_meters = parse_carla_depth(depth_camera.rgb_image)
        pos_x, pos_y = pygame.mouse.get_pos()
        click_point = np.array([pos_x, pos_y, 1])
        intrinsic = camera.camera_actor.intrinsic
        
        click_point_3d = np.dot(np.linalg.inv(intrinsic), click_point)
        click_point_3d *= depth_in_meters[pos_y, pos_x]
        
        y,z,x = click_point_3d
        z = -z
        
        click_point_3d = np.array([x,y,z, 1])
        click_point_3d.reshape((4,1))
        
        camera_rt = compute_extrinsic_from_transform(camera.camera_actor.get_transform())
        
        click_point_world_3d = np.dot(camera_rt, click_point_3d)
        
        return click_point_world_3d.tolist()[0][:3]

def parse_carla_depth(depth_image):
  """Parse Carla depth image."""
  # 0.9.6: The image codifies the depth in 3 channels of the RGB color space,
  # from less to more significant bytes: R -> G -> B.
  # depth_image is [h, w, 3], last dim is RGB order
  depth_image = depth_image.astype("float32")
  normalized = (depth_image[:, :, 0] + depth_image[:, :, 1]*256 + \
      depth_image[:, :, 2]*256*256) / (256 * 256 * 256 - 1)
  return 1000 * normalized


def compute_intrinsic(img_width, img_height, fov):
  """Compute intrinsic matrix."""
  intrinsic = np.identity(3)
  intrinsic[0, 2] = img_width / 2.0
  intrinsic[1, 2] = img_height / 2.0
  intrinsic[0, 0] = intrinsic[1, 1] = img_width / (2.0 * np.tan(fov *
                                                                np.pi / 360.0))
  return intrinsic


def compute_extrinsic_from_transform(transform_):
  """
  Creates extrinsic matrix from carla transform.
  This is known as the coordinate system transformation matrix.
  """

  rotation = transform_.rotation
  location = transform_.location
  c_y = np.cos(np.radians(rotation.yaw))
  s_y = np.sin(np.radians(rotation.yaw))
  c_r = np.cos(np.radians(rotation.roll))
  s_r = np.sin(np.radians(rotation.roll))
  c_p = np.cos(np.radians(rotation.pitch))
  s_p = np.sin(np.radians(rotation.pitch))
  matrix = np.matrix(np.identity(4))  # matrix is needed
  # 3x1 translation vector
  matrix[0, 3] = location.x
  matrix[1, 3] = location.y
  matrix[2, 3] = location.z
  # 3x3 rotation matrix
  matrix[0, 0] = c_p * c_y
  matrix[0, 1] = c_y * s_p * s_r - s_y * c_r
  matrix[0, 2] = -c_y * s_p * c_r - s_y * s_r
  matrix[1, 0] = s_y * c_p
  matrix[1, 1] = s_y * s_p * s_r + c_y * c_r
  matrix[1, 2] = -s_y * s_p * c_r + c_y * s_r
  matrix[2, 0] = s_p
  matrix[2, 1] = -c_p * s_r
  matrix[2, 2] = c_p * c_r
  # [3, 3] == 1, rest is zero
  return matrix





