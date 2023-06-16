import json
import atexit

# Load camera configurations from JSON file
with open('camera_configs.json') as config_file:
    camera_configs = json.load(config_file)

# Extract variables from camera_configs dictionary
source_matrix_depth_factor_v = camera_configs["source_matrix_depth_factor_v"]
source_matrix_depth_factor_h = camera_configs["source_matrix_depth_factor_h"]
destination_matrix_depth_factor_v = camera_configs["destination_matrix_depth_factor_v"]
destination_matrix_depth_factor_h = camera_configs["destination_matrix_depth_factor_h"]
wrapped_image_dimensions_vertical = camera_configs["wrapped_image_dimensions_vertical"]
wrapped_image_dimensions_horizontal = camera_configs["wrapped_image_dimensions_horizontal"]
pygame_window_dimensions = camera_configs["pygame_window_dimensions"]
front_camera_left_indentation = camera_configs["front_camera_left_indentation"]
front_camera_top_indentation = camera_configs["front_camera_top_indentation"]
right_camera_left_indentation = camera_configs["right_camera_left_indentation"]
right_camera_top_indentation = camera_configs["right_camera_top_indentation"]
rear_camera_left_indentation = camera_configs["rear_camera_left_indentation"]
rear_camera_top_indentation = camera_configs["rear_camera_top_indentation"]
left_camera_top_indentation = camera_configs["left_camera_top_indentation"]
left_camera_left_indentation = camera_configs["left_camera_left_indentation"]

def get_source_matrix(id, h, w):
    if id == 1 or id == 3:
        return [[0, h//source_matrix_depth_factor_v], [w, h//source_matrix_depth_factor_v], [w, h], [0, h]]
    else:
        return [[0, h//source_matrix_depth_factor_h], [w, h//source_matrix_depth_factor_h], [w, h], [0, h]]

def get_destination_matrix(id, h, w):
    if id == 1 or id == 3:
        return [[0, 0], [w, 0], [(w//2)+(w//destination_matrix_depth_factor_v), h], [(w//2)-(w//destination_matrix_depth_factor_v), h]]
    else:
        return [[0, 0], [w, 0], [(w//2)+(w//destination_matrix_depth_factor_h), h], [(w//2)-(w//destination_matrix_depth_factor_h), h]]

def get_wrapped_image_dimensions(id):
    if id == 1 or id == 3:
        return wrapped_image_dimensions_vertical
    else:
        return wrapped_image_dimensions_horizontal

pygame_images_window_placement={
    '1': (pygame_window_dimensions['w']//front_camera_left_indentation, pygame_window_dimensions['h']//front_camera_top_indentation),
    '2': (pygame_window_dimensions['w']*2//right_camera_left_indentation, right_camera_top_indentation),
    '3': (pygame_window_dimensions['w']//rear_camera_left_indentation, pygame_window_dimensions['h']*2//rear_camera_top_indentation),
    '4': (left_camera_left_indentation, left_camera_top_indentation)
}

def save_camera_configs():
    # Create a dictionary with the variable values
    camera_configs = {
        "source_matrix_depth_factor_v": source_matrix_depth_factor_v,
        "source_matrix_depth_factor_h": source_matrix_depth_factor_h,
        "destination_matrix_depth_factor_v": destination_matrix_depth_factor_v,
        "destination_matrix_depth_factor_h": destination_matrix_depth_factor_h,
        "wrapped_image_dimensions_vertical": wrapped_image_dimensions_vertical,
        "wrapped_image_dimensions_horizontal": wrapped_image_dimensions_horizontal,
        "pygame_window_dimensions": pygame_window_dimensions,
        "front_camera_left_indentation": front_camera_left_indentation,
        "front_camera_top_indentation": front_camera_top_indentation,
        "right_camera_left_indentation": right_camera_left_indentation,
        "right_camera_top_indentation": right_camera_top_indentation,
        "rear_camera_left_indentation": rear_camera_left_indentation,
        "rear_camera_top_indentation": rear_camera_top_indentation,
        "left_camera_top_indentation": left_camera_top_indentation,
        "left_camera_left_indentation": left_camera_left_indentation
    }

    # Save the camera_configs dictionary to the JSON file
    with open('camera_configs.json', 'w') as config_file:
        json.dump(camera_configs, config_file, indent=4)

def update_source_matrix_vertical(new_val):
    global source_matrix_depth_factor_v
    source_matrix_depth_factor_v = float(new_val)

def update_source_matrix_horizontal(new_val):
    global source_matrix_depth_factor_h
    source_matrix_depth_factor_h = float(new_val)
    
def update_destination_matrix_vertical(new_val):
    global destination_matrix_depth_factor_v
    destination_matrix_depth_factor_v = float(new_val)

def update_destination_matrix_horizontal(new_val):
    global destination_matrix_depth_factor_h
    destination_matrix_depth_factor_h = float(new_val)

def update_wrapped_image_dimensions_vertical_h(new_val):
    wrapped_image_dimensions_vertical["h"] = int(float(new_val))

def update_wrapped_image_dimensions_vertical_w(new_val):
    wrapped_image_dimensions_vertical['w'] = int(float(new_val))

def update_wrapped_image_dimensions_horizontal_h(new_val):
    wrapped_image_dimensions_horizontal['h'] = int(float(new_val))

def update_wrapped_image_dimensions_horizontal_w(new_val):
    wrapped_image_dimensions_horizontal['w'] = int(float(new_val))

def update_front_camera_left_indentation(new_val):
    front_camera_left_indentation = float(new_val)
    pygame_images_window_placement['1'] = (pygame_window_dimensions['w']//front_camera_left_indentation, pygame_window_dimensions['h']//front_camera_top_indentation)

def update_front_camera_top_indentation(new_val):
    front_camera_top_indentation = float(new_val)
    pygame_images_window_placement['1'] = (pygame_window_dimensions['w']//front_camera_left_indentation, pygame_window_dimensions['h']//front_camera_top_indentation)

def update_right_camera_left_indentation(new_val):
    right_camera_left_indentation = float(new_val)
    pygame_images_window_placement['2'] = (pygame_window_dimensions['w']*2//right_camera_left_indentation, right_camera_top_indentation)

def update_right_camera_top_indentation(new_val):
    right_camera_top_indentation = float(new_val)
    pygame_images_window_placement['2'] = (pygame_window_dimensions['w']*2//right_camera_left_indentation, right_camera_top_indentation)

def update_rear_camera_left_indentation(new_val):
    rear_camera_left_indentation = float(new_val)
    pygame_images_window_placement['3'] = (pygame_window_dimensions['w']//rear_camera_left_indentation, pygame_window_dimensions['h']*2//rear_camera_top_indentation)

def update_rear_camera_top_indentation(new_val):
    rear_camera_top_indentation = float(new_val)
    pygame_images_window_placement['3'] = (pygame_window_dimensions['w']//rear_camera_left_indentation, pygame_window_dimensions['h']*2//rear_camera_top_indentation)

def update_left_camera_left_indentation(new_val):
    left_camera_left_indentation = float(new_val)
    pygame_images_window_placement['4'] = (left_camera_left_indentation, left_camera_top_indentation)

def update_left_camera_top_indentation(new_val):
    left_camera_top_indentation = float(new_val)
    pygame_images_window_placement['4'] = (left_camera_left_indentation, left_camera_top_indentation)


# Call the save_camera_configs function before program exit
atexit.register(save_camera_configs)

