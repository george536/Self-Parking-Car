import cv2
import numpy as np
from camera_config import *
from pygame.locals import *
import pygame

images = [None, None, None, None]

def raw_data_to_image(image):
    # Convert image data to a NumPy array
    image_array = np.array(image.raw_data)

    # Reshape the image array to the desired dimensions
    image_reshaped = image_array.reshape((image.height, image.width, 4))

    # Return the image array
    return image_reshaped


def get_srouce_and_destination_matrices(id, image):
    # Define the source points for the perspective transform
    source_points = np.float32(get_source_matrix(image.height, image.width))

    new_dimensions = get_wrapped_image_dimensions(id)

    destination_points = np.float32(get_destination_matrix(new_dimensions['h'],new_dimensions['w']))

    return source_points, destination_points


def transform_perspective(id, image_reshaped, source_points, destination_points):
    
    # Compute the perspective transform matrix
    perspective_matrix = cv2.getPerspectiveTransform(source_points, destination_points)

    new_dimensions = get_wrapped_image_dimensions(id)

    # Perform the perspective transform
    transformed_image = cv2.warpPerspective(image_reshaped, perspective_matrix, (new_dimensions['w'],new_dimensions['h']))

    return transformed_image


def combine_images(combined_surface):

    global images
    id = 0
    for image in images:
        id +=1 
    
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pygame_img = pygame.surfarray.make_surface(image_rgb)
        #pygame_img = pygame.image.frombuffer(pygame_img.tostring(), pygame_img.shape[1::-1], "BGR")
        if id == 1 or id == 3:
            pygame_img = pygame.transform.rotate(pygame_img, 270)
        elif id == 2:
            pygame_img = pygame.transform.rotate(pygame_img, 180)
        else:
            pygame_img = pygame.transform.rotate(pygame_img, 0)
        pygame_img.set_colorkey((0,0,0))
        pygame_img.set_alpha(255)
        combined_surface.blit(pygame_img, pygame_images_window_placement[str(id)])


def generate_birds_eye_view(id, image, combined_surface):

    image_reshaped = raw_data_to_image(image)

    source_points, destination_points = get_srouce_and_destination_matrices(id, image)

    transformed_image = transform_perspective(id, image_reshaped, source_points, destination_points)

    if id == 3:
        transformed_image = cv2.flip(transformed_image, 0)

    if id == 4:
        transformed_image = cv2.flip(transformed_image, 1)

    if id == 2:
        transformed_image = cv2.flip(transformed_image, 3)

    if id == 1:
        transformed_image = cv2.flip(transformed_image, 4)

    images[id-1] = transformed_image

    if all(item is not None for item in images):
        combine_images(combined_surface)

    # cv2.imshow(str(id), rotated_image)
    # cv2.waitKey(10)