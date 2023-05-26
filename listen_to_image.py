import cv2
import numpy as np

def process_image(id, image, im_height, im_width):
    i = np.array(image.raw_data)
    i2 = i.reshape((im_height, im_width, 4))
    i3 = i2[:, :, :3]
    cv2.imshow(str(id), i3)
    cv2.waitKey(1)
    return i3/255.0

x1, y1 = 100, 100  # Top-left corner
x2, y2 = 200, 100  # Top-right corner
x3, y3 = 300, 200  # Bottom-right corner
x4, y4 = 0, 200    # Bottom-left corner

images = [None, None, None, None]

def combine_images(im_height, im_width):

    h = im_height
    w = im_width

    # Create a canvas to combine the images
    canvas_width = w * 3
    canvas_height = h * 3
    canvas = np.zeros((canvas_height, canvas_width, 4), dtype=np.uint8)

    # Place the images onto the canvas
    canvas[h//2:h+h//2, 0:w] = images[3] # left
    canvas[0:h, w:w*2] = images[0] # front
    canvas[int(h*1.5):int(h*2.5), w:w*2] = images[2] # rear
    canvas[h//2:h+h//2, w*2:w*3] = images[1] # right

    cv2.imshow("Bird's eye view", canvas)
    cv2.waitKey(10)

def perspective_transform(id, image, im_height, im_width):
    # Define the source points for the perspective transform
    source_points = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

    offset = 50  # Define an offset to create some space around the transformed image
    destination_points = np.float32([[offset, offset], [im_width-offset, offset], [im_width-offset, im_height-offset], [offset, im_height-offset]])

    # Compute the perspective transform matrix
    perspective_matrix = cv2.getPerspectiveTransform(source_points, destination_points)

    # Convert image data to a NumPy array
    image_array = np.array(image.raw_data)

    # Reshape the image array to the desired dimensions
    image_reshaped = image_array.reshape((im_height, im_width, 4))

    # Perform the perspective transform
    transformed_image = cv2.warpPerspective(image_reshaped, perspective_matrix, (im_width, im_height))

    # Calculate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D((im_width/2, im_height/2), -(id-1)*90, 1)

    # Apply the rotation to the image
    rotated_image = cv2.warpAffine(transformed_image, rotation_matrix, (im_width, im_height))

    images[id-1] = rotated_image
    
    if all(item is not None for item in images):
        combine_images(im_height, im_width)
    #cv2.imshow(str(id), rotated_image)
    #cv2.waitKey(10)

    return transformed_image, rotated_image