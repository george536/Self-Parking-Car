import cv2
import numpy as np
from birds_eye_view.camera_configs_modifier import *
from pygame.locals import *
import pygame
from threading import Semaphore

from birds_eye_view.combined_surface import get_combined_surface, semaphore


semaphore_surface = Semaphore(1)

images = [None, None, None, None]
count = 0
config_modifications_instance = ConfigModifier.get_instance()

def raw_data_to_image(image):
    # Convert image data to a NumPy array
    image_array = np.array(image.raw_data)

    # Reshape the image array to the desired dimensions
    image_reshaped = image_array.reshape((image.height, image.width, 4))

    # Return the image array
    return image_reshaped


def get_srouce_and_destination_matrices(id, image):
    # Define the source points for the perspective transform
    source_points = np.float32(get_source_matrix(id, image.height, image.width))

    new_dimensions = get_wrapped_image_dimensions(id)

    destination_points = np.float32(get_destination_matrix(id, new_dimensions['h'],new_dimensions['w']))

    return source_points, destination_points


def transform_perspective(id, image_reshaped, source_points, destination_points):
    
    # Compute the perspective transform matrix
    perspective_matrix = cv2.getPerspectiveTransform(source_points, destination_points)

    new_dimensions = get_wrapped_image_dimensions(id)

    # Perform the perspective transform
    transformed_image = cv2.warpPerspective(image_reshaped, perspective_matrix, (new_dimensions['w'],new_dimensions['h']))

    return transformed_image

def get_surface_image(id, image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pygame_img = pygame.surfarray.make_surface(image_rgb)
    
    if id == 1 or id == 2:
            pygame_img = pygame.transform.rotate(pygame_img, 270)
    elif id == 3:
        pygame_img = pygame.transform.rotate(pygame_img, 180)
    else:
        pygame_img = pygame.transform.rotate(pygame_img, 0)
    
    pygame_img.set_colorkey((0,0,0))
    pygame_img.set_alpha(255)
    
    return pygame_img

def combine_images():

    global images
    
    semaphore.acquire()
    combined_surface = get_combined_surface()
    
    combined_surface.fill((0,0,0))
    
    top_image = get_surface_image(1, images[0])
    bottom_image = get_surface_image(2, images[1])
    left_image = get_surface_image(3, images[2])
    right_image = get_surface_image(4, images[3])
    
    
    combined_surface.blit(left_image, config_modifications_instance.pygame_images_window_placement['3'])
    combined_surface.blit(right_image, config_modifications_instance.pygame_images_window_placement['4'])
    combined_surface.blit(top_image, config_modifications_instance.pygame_images_window_placement['1'])
    combined_surface.blit(bottom_image, config_modifications_instance.pygame_images_window_placement['2'])
    

    global count
    count = 0


    #################### Middle Rectangle begin ###################
    # Determine the dimensions of the rectangle
    rect_width = 35 * 2
    rect_height = 88 * 2

    # Calculate the top-left corner coordinates
    rect_x = (config_modifications_instance.pygame_window_dimensions['w'] - rect_width) // 2
    rect_y = (config_modifications_instance.pygame_window_dimensions['h'] - rect_height) // 2

    # Create the rectangle object
    rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)

    # Set the color of the rectangle
    rect_color = (0, 0, 255)  # Red

    # Draw the rectangle on the combined surface
    pygame.draw.rect(combined_surface, rect_color, rect)
    #################### Middle Rectangle end ###################
    
    semaphore.release()


def generate_birds_eye_view(id, image):

    image_reshaped = raw_data_to_image(image)

    source_points, destination_points = get_srouce_and_destination_matrices(id, image)

    transformed_image = transform_perspective(id, image_reshaped, source_points, destination_points)

    if id == 2:
        transformed_image = cv2.flip(transformed_image, 0)

    if id == 4:
        transformed_image = cv2.flip(transformed_image, 1)

    if id == 3:
        transformed_image = cv2.flip(transformed_image, 3)

    if id == 1:
        transformed_image = cv2.flip(transformed_image, 4)

    images[id-1] = transformed_image

    global count
    count+=1
    
    cv2.imshow('Birds Eye View ' + str(id), image_reshaped)
    cv2.waitKey(1)
    
    if all(item is not None for item in images) and count >=3:
        combine_images()
