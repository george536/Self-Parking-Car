import cv2
import numpy as np

def process_image(image, im_height, im_width):
    i = np.array(image.raw_data)
    i2 = i.reshape((im_height, im_width, 4))
    i3 = i2[:, :, :3]
    cv2.imshow("", i3)
    cv2.waitKey(1)
    return i3/255.0

x1, y1 = 200, 200  # Top-left corner
x2, y2 = 400, 200  # Top-right corner
x3, y3 = 600, 400  # Bottom-right corner
x4, y4 = 0, 400    # Bottom-left corner

def perspective_transform(image, im_height, im_width):
    # Define the source points for the perspective transform
    source_points = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

    offset = 75  # Define an offset to create some space around the transformed image
    destination_points = np.float32([[offset, offset], [im_width-offset, offset], [im_width-offset, im_height-offset], [offset, im_height-offset]])

    # Compute the perspective transform matrix
    perspective_matrix = cv2.getPerspectiveTransform(source_points, destination_points)

    # Convert image data to a NumPy array
    image_array = np.array(image.raw_data)

    # Reshape the image array to the desired dimensions
    image_reshaped = image_array.reshape((image.height, image.width, 4))

    # Perform the perspective transform
    transformed_image = cv2.warpPerspective(image_reshaped, perspective_matrix, (im_width, im_height))

    cv2.imshow("", transformed_image)
    cv2.waitKey(1)

    return transformed_image