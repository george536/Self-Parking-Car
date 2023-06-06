
def get_source_matrix(h, w):
    return [[0, h//2.5], [w, h//2.5], [w, h], [0, h]]

def get_destination_matrix(h, w):
    return [[0, 0], [w, 0], [(w//2)+(w//4), h], [(w//2)-(w//4), h]]

# scaled size down to area of interest for birds eye view
wrapped_image_dimensions_vertical = {
    'w' : 320,
    'h' : 240
}

wrapped_image_dimensions_horizontal = {
    'w' : 700,
    'h' : 240
}

def get_wrapped_image_dimensions(id):
    if id == 1 or id == 3:
        return wrapped_image_dimensions_vertical
    else:
        return wrapped_image_dimensions_horizontal
    
rotation_angles = {
    '1' : 0,
    '2' : 90,
    '3' : 180,
    '4' : -90
}

# This is windows size for rotated images as it requires different image size
rotated_image_dimensions_vertical = {
    'w' : 320,
    'h' : 240
}

rotated_image_dimensions_horizontal = {
    'w' : 240,
    'h' : 700
}

def get_rotated_image_dimensions(id):
    if id == 1 or id == 3:
        return rotated_image_dimensions_vertical
    else:
        return rotated_image_dimensions_horizontal