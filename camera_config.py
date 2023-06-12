source_matrix_depth_factor = 2.7
def get_source_matrix(h, w):
    return [[0, h//source_matrix_depth_factor], [w, h//source_matrix_depth_factor], [w, h], [0, h]]

destination_matrix_depth_factor = 25
def get_destination_matrix(h, w):

    return [[0, 0], [w, 0], [(w//2)+(w//destination_matrix_depth_factor), h], [(w//2)-(w//destination_matrix_depth_factor), h]]

# scaled size down to area of interest for birds eye view
wrapped_image_dimensions_vertical = {
    'w' : 400,
    'h' : 200
}

wrapped_image_dimensions_horizontal = {
    'w' : 500,
    'h' : 250
}

def get_wrapped_image_dimensions(id):
    if id == 1 or id == 3:
        return wrapped_image_dimensions_vertical
    else:
        return wrapped_image_dimensions_horizontal
    
pygame_window_dimensions = {
    'w':500,
    'h' : 500
}

front_camera_left_indentation = 7.5
front_camera_top_indentation = 20
right_camera_left_indentation = 3.3
rear_camera_left_indentation = 7.5
rear_camera_top_indentation = 3.5
pygame_images_window_placement={
    '1' : (pygame_window_dimensions['w']//front_camera_left_indentation, pygame_window_dimensions['h']//front_camera_top_indentation),
    '2' : (pygame_window_dimensions['w']*2//right_camera_left_indentation, 0),
    '3' : (pygame_window_dimensions['w']//rear_camera_left_indentation, pygame_window_dimensions['h']*2//rear_camera_top_indentation),
    '4' : (0, 0)
}