import cv2
import numpy as np
from pygame.locals import *
import pygame
from camera_config import *

# pygame.init()
# window_size = (800, 600)  # Set your desired window size
# window = pygame.display.set_mode(window_size)

images = [None, None, None, None]
active = False

def process_image(id, image, im_height, im_width):
    i = np.array(image.raw_data)
    i2 = i.reshape((im_height, im_width, 4))
    i3 = i2[:, :, :3]
    cv2.imshow(str(id), i3)
    cv2.waitKey(1)
    return i3/255.0

def combine_images(h, w):
    global active
    if not active:
        active = True

        # Create a canvas to combine the images
        canvas_width = w * 3
        canvas_height = int(h * 2.5)
        canvas = np.zeros((canvas_height, canvas_width, 4), dtype=np.uint8)

        gray = cv2.cvtColor(images[3], cv2.COLOR_BGR2GRAY)

        # Apply thresholding to the grayscale image
        _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

        # Split the channels of the colored image
        # Split the channels of the image
        channels = cv2.split(images[3])

        # Access the individual channels using array indexing
        b = channels[0]
        g = channels[1]
        r = channels[2]

        # Create a new alpha channel with the binary image
        alpha = cv2.merge((b, g, r, binary))

        # Merge the new alpha channel with the original image
        result = cv2.cvtColor(alpha, cv2.COLOR_BGRA2BGR)

        # Place the images onto the canvas
        # canvas[0:h, w:w*2] = images[0] # front
        # canvas[int(h*1.5):int(h*2.5), w:w*2] = images[2] # rear
        canvas[int(0.3*h) + h//2:int(0.3*h) +h+h//2, w//3:w+w//3, :3] = result # left
        canvas[int(0.3*h) + h//2:int(0.3*h) +h+h//2, w*2 - w//3:w*3 - w//3] = images[1] # right

        cv2.imshow("Bird's eye view", canvas)
        cv2.waitKey(10)

        active = False

    # combined_surface = pygame.Surface(window_size, pygame.SRCALPHA)
    # image_np = np.asarray(images[0], dtype=np.uint8)
    # # Reshape the array to a 2D array
    # arr_2d = np.reshape(images[0], (3072, 100))
    # combined_surface.blit(pygame.surfarray.make_surface(arr_2d), (0, 0))  # front
    # # combined_surface.blit(pygame.surfarray.make_surface(images[1]), (w, 0))  # right
    # # combined_surface.blit(pygame.surfarray.make_surface(images[2]), (w, int(h * 1.5)))  # rear
    # # combined_surface.blit(pygame.surfarray.make_surface(images[3]), (w * 2, 0))  # left


    # window.blit(combined_surface, (0, 0))
    # pygame.display.update()


def perspective_transform(id, image, im_height, im_width, scaled_h, scaled_w):

    # Define the source points for the perspective transform
    source_points = np.float32(get_source_matrix(im_height, im_width))

    destination_points = np.float32(get_destination_matrix(scaled_h,scaled_w))

    # Compute the perspective transform matrix
    perspective_matrix = cv2.getPerspectiveTransform(source_points, destination_points)

    # Convert image data to a NumPy array
    image_array = np.array(image.raw_data)

    # Reshape the image array to the desired dimensions
    image_reshaped = image_array.reshape((scaled_h, scaled_w, 4))

    # Perform the perspective transform
    transformed_image = cv2.warpPerspective(image_reshaped, perspective_matrix, (scaled_w, scaled_h))

    # Calculate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D((scaled_w/2, scaled_h/2), -(id-1)*90, 1)

    # Apply the rotation to the image
    rotated_image = cv2.warpAffine(transformed_image, rotation_matrix, (scaled_w, scaled_h))

    images[id-1] = rotated_image
    
    if all(item is not None for item in images):
        combine_images(im_height, im_width)

    return transformed_image, rotated_image