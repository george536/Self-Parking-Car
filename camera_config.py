
def get_source_matrix(h, w):
    # used to be 2.5
    return [[0, h//2.7], [w, h//2.7], [w, h], [0, h]]

def get_destination_matrix(h, w):
    # used to be 20
    return [[0, 0], [w, 0], [(w//2)+(w//25), h], [(w//2)-(w//25), h]]

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


pygame_images_window_placement={
    '1' : (pygame_window_dimensions['w']//7.5, pygame_window_dimensions['h']//20),
    '2' : (pygame_window_dimensions['w']*2//3.3, 0),
    '3' : (pygame_window_dimensions['w']//7.5, pygame_window_dimensions['h']*2//3.5),
    '4' : (0, 0)
}