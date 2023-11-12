from threading import Semaphore
from  cv2 import getPerspectiveTransform
from  cv2 import warpPerspective
from  cv2 import COLOR_BGR2RGB
from  cv2 import cvtColor
from  cv2 import flip
import numpy as np
import pygame
from birds_eye_view.camera_configs_modifier import *
from birds_eye_view.comb_surface_access import get_combined_surface, combined_surface_semaphore
from pygame.locals import *

surface_semaphore = Semaphore(1)

images = [None, None, None, None]
count = 0
CONFIG_MODIFICATIONS_INSTANCE = ConfigModifier.get_instance()

def raw_data_to_image(image):
    """Resize the image to be of desired size"""
    # Convert image data to a NumPy array
    image_array = np.array(image.raw_data)

    # Reshape the image array to the desired dimensions
    image_reshaped = image_array.reshape((image.height, image.width, 4))

    # Return the image array
    return image_reshaped


def get_srouce_and_destination_matrices(camera_id, image):
    """Gets the source image matrix size and the desired destination for bird's eye view"""
    # Define the source points for the perspective transform
    source_points = np.float32(get_source_matrix(camera_id, image.height, image.width))

    new_dimensions = get_wrapped_image_dimensions(camera_id)

    destination_points = np.float32(get_destination_matrix(
        camera_id, new_dimensions['h'],new_dimensions['w']))

    return source_points, destination_points


def transform_perspective(camera_id, image_reshaped, source_points, destination_points):
    """Transforms the image of source matrix into destination one"""
    # Compute the perspective transform matrix
    perspective_matrix = getPerspectiveTransform(source_points, destination_points)

    new_dimensions = get_wrapped_image_dimensions(camera_id)

    # Perform the perspective transform
    transformed_image = warpPerspective(image_reshaped, perspective_matrix,
                                        (new_dimensions['w'],new_dimensions['h']))

    return transformed_image

def get_surface_image(camera_id, image):
    """Get image data as pygame surface"""
    image_rgb = cvtColor(image, COLOR_BGR2RGB)
    pygame_img = pygame.surfarray.make_surface(image_rgb)

    if camera_id == 1 or camera_id == 2:
        pygame_img = pygame.transform.rotate(pygame_img, 270)
    elif camera_id == 3:
        pygame_img = pygame.transform.rotate(pygame_img, 180)
    else:
        pygame_img = pygame.transform.rotate(pygame_img, 0)

    pygame_img.set_colorkey((0,0,0))
    pygame_img.set_alpha(255)

    return pygame_img

def combine_images():
    """Combines all 4 images to form the bird's eye view in one surface"""
    global images

    combined_surface_semaphore.acquire()
    combined_surface = get_combined_surface()

    combined_surface.fill((0,0,0))

    top_image = get_surface_image(1, images[0])
    bottom_image = get_surface_image(2, images[1])
    left_image = get_surface_image(3, images[2])
    right_image = get_surface_image(4, images[3])

    combined_surface.blit(top_image,
                          CONFIG_MODIFICATIONS_INSTANCE.pygame_images_window_placement['1'])
    combined_surface.blit(bottom_image,
                          CONFIG_MODIFICATIONS_INSTANCE.pygame_images_window_placement['2'])
    combined_surface.blit(left_image,
                          CONFIG_MODIFICATIONS_INSTANCE.pygame_images_window_placement['3'])
    combined_surface.blit(right_image,
                          CONFIG_MODIFICATIONS_INSTANCE.pygame_images_window_placement['4'])

    global count
    count = 0

    combined_surface_semaphore.release()


def generate_birds_eye_view(camera_id, image):
    """Prepares all 4 images to be combined"""
    image_reshaped = raw_data_to_image(image)

    source_points, destination_points = get_srouce_and_destination_matrices(camera_id, image)

    transformed_image = transform_perspective(
        camera_id, image_reshaped, source_points, destination_points)

    if camera_id == 2:
        transformed_image = flip(transformed_image, 0)

    if camera_id == 4:
        transformed_image = flip(transformed_image, 1)

    if camera_id == 3:
        transformed_image = flip(transformed_image, 3)

    if camera_id == 1:
        transformed_image = flip(transformed_image, 4)

    images[camera_id-1] = transformed_image

    global count
    count+=1

    if all(item is not None for item in images) and count >=3:
        combine_images()
