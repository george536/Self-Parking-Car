import cv2
import numpy as np
from camera_config import *

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

def rotate_image(id, image, transformed_image):

    # Calculate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D((image.width/2, image.height/2), -rotation_angles[str(id)], 1)


    new_rotated_dimensions = get_rotated_image_dimensions(id)

    # Apply the rotation to the image
    rotated_image = cv2.warpAffine(transformed_image, rotation_matrix, (new_rotated_dimensions['w'], new_rotated_dimensions['h']))

    return rotated_image

def generate_birds_eye_view(id, image):

    image_reshaped = raw_data_to_image(image)

    source_points, destination_points = get_srouce_and_destination_matrices(id, image)

    transformed_image = transform_perspective(id, image_reshaped, source_points, destination_points)

    rotated_image = rotate_image(id, image, transformed_image)

    cv2.imshow(str(id), rotated_image)
    cv2.waitKey(10)