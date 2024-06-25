import json
import atexit

def get_source_matrix(camera_id, h, w):
    config_modifications_insatnce = ConfigModifier.get_instance()
    if camera_id == 1 or camera_id == 2:
        return [[0, h//config_modifications_insatnce.source_matrix_depth_factor_v],
                [w, h//config_modifications_insatnce.source_matrix_depth_factor_v],
                [w, h], [0, h]]
    
    if camera_id == 5:
        return [[0, h//config_modifications_insatnce.source_matrix_depth_factor_top_down],
                [w, h//config_modifications_insatnce.source_matrix_depth_factor_top_down],
                [w, h], [0, h]]

    else:
        return [[0, h//config_modifications_insatnce.source_matrix_depth_factor_h],
                [w, h//config_modifications_insatnce.source_matrix_depth_factor_h],
                [w, h], [0, h]]

def get_destination_matrix(camera_id, h, w):
    config_modifications_insatnce = ConfigModifier.get_instance()
    if camera_id in (1,2):
        return [[0, 0], [w, 0],
                [(w//2)+(w//config_modifications_insatnce.destination_matrix_depth_factor_v), h],
                [(w//2)-(w//config_modifications_insatnce.destination_matrix_depth_factor_v), h]]
    
    if camera_id == 5:
        return [[0, 0], [w, 0],
                [(w//2)+(w//config_modifications_insatnce.destination_matrix_depth_factor_top_down), h],
                [(w//2)-(w//config_modifications_insatnce.destination_matrix_depth_factor_top_down), h]]

    return [[0, 0], [w, 0],
            [(w//2)+(w//config_modifications_insatnce.destination_matrix_depth_factor_h), h],
            [(w//2)-(w//config_modifications_insatnce.destination_matrix_depth_factor_h), h]]

def get_wrapped_image_dimensions(camera_id):
    config_modifications_insatnce = ConfigModifier.get_instance()
    if camera_id in (1,2):
        return config_modifications_insatnce.wrapped_image_dimensions_vertical
    
    if camera_id == 5:
        return config_modifications_insatnce.wrapped_image_dimensions_top_down

    return config_modifications_insatnce.wrapped_image_dimensions_horizontal

class ConfigModifier:
    __instance = None

    @staticmethod
    def get_instance():
        if ConfigModifier.__instance is None:
            ConfigModifier()
        return ConfigModifier.__instance

    def __init__(self):
        if ConfigModifier.__instance is None:
            self.load_data()
            self.assing_variables()
            ConfigModifier.__instance = self
            self.camera_configs = {}

    def load_data(self):
        print("loading Bird's Eye View configurations..")
        # Load camera configurations from JSON file
        with open('birds_eye_view/camera_configs.json', encoding="utf-8") as config_file:
            self.camera_configs = json.load(config_file)

    def assing_variables(self):
        # Extract variables from camera_configs dictionary
        self.source_matrix_depth_factor_v = self.camera_configs["source_matrix_depth_factor_v"]
        self.source_matrix_depth_factor_h = self.camera_configs["source_matrix_depth_factor_h"]
        self.source_matrix_depth_factor_top_down = self.camera_configs["source_matrix_depth_factor_top_down"]
        self.destination_matrix_depth_factor_v = self.camera_configs["destination_matrix_depth_factor_v"]
        self.destination_matrix_depth_factor_h = self.camera_configs["destination_matrix_depth_factor_h"]
        self.destination_matrix_depth_factor_top_down = self.camera_configs["destination_matrix_depth_factor_top_down"]
        self.wrapped_image_dimensions_vertical = self.camera_configs["wrapped_image_dimensions_vertical"]
        self.wrapped_image_dimensions_horizontal = self.camera_configs["wrapped_image_dimensions_horizontal"]
        self.wrapped_image_dimensions_top_down = self.camera_configs["wrapped_image_dimensions_top_down"]
        self.pygame_window_dimensions = self.camera_configs["pygame_window_dimensions"]
        self.front_camera_left_indentation = self.camera_configs["front_camera_left_indentation"]
        self.front_camera_top_indentation = self.camera_configs["front_camera_top_indentation"]
        self.right_camera_left_indentation = self.camera_configs["right_camera_left_indentation"]
        self.right_camera_top_indentation = self.camera_configs["right_camera_top_indentation"]
        self.rear_camera_left_indentation = self.camera_configs["rear_camera_left_indentation"]
        self.rear_camera_top_indentation = self.camera_configs["rear_camera_top_indentation"]
        self.left_camera_top_indentation = self.camera_configs["left_camera_top_indentation"]
        self.left_camera_left_indentation = self.camera_configs["left_camera_left_indentation"]
        self.pygame_images_window_placement={
        '1': (self.pygame_window_dimensions['w']//self.front_camera_left_indentation, 
              self.pygame_window_dimensions['h']//self.front_camera_top_indentation),
        '3': (self.pygame_window_dimensions['w']*2//self.right_camera_left_indentation, 
              self.right_camera_top_indentation),
        '2': (self.pygame_window_dimensions['w']//self.rear_camera_left_indentation, 
              self.pygame_window_dimensions['h']*2//self.rear_camera_top_indentation),
        '4': (self.left_camera_left_indentation, self.left_camera_top_indentation)
        }

    def save_camera_configs(self):
        print("saving Bird's Eye View configurations..")
        # Create a dictionary with the variable values
        self.camera_configs = {
            "source_matrix_depth_factor_v": self.source_matrix_depth_factor_v,
            "source_matrix_depth_factor_h": self.source_matrix_depth_factor_h,
            "source_matrix_depth_factor_top_down": self.source_matrix_depth_factor_top_down,
            "destination_matrix_depth_factor_v": self.destination_matrix_depth_factor_v,
            "destination_matrix_depth_factor_h": self.destination_matrix_depth_factor_h,
            "destination_matrix_depth_factor_top_down": self.destination_matrix_depth_factor_top_down,
            "wrapped_image_dimensions_vertical": self.wrapped_image_dimensions_vertical,
            "wrapped_image_dimensions_horizontal": self.wrapped_image_dimensions_horizontal,
            "wrapped_image_dimensions_top_down": self.wrapped_image_dimensions_top_down,
            "pygame_window_dimensions": self.pygame_window_dimensions,
            "front_camera_left_indentation": self.front_camera_left_indentation,
            "front_camera_top_indentation": self.front_camera_top_indentation,
            "right_camera_left_indentation": self.right_camera_left_indentation,
            "right_camera_top_indentation": self.right_camera_top_indentation,
            "rear_camera_left_indentation": self.rear_camera_left_indentation,
            "rear_camera_top_indentation": self.rear_camera_top_indentation,
            "left_camera_top_indentation": self.left_camera_top_indentation,
            "left_camera_left_indentation": self.left_camera_left_indentation
        }

        # Save the camera_configs dictionary to the JSON file
        with open('birds_eye_view/camera_configs.json', 'w', encoding="utf-8") as config_file:
            json.dump(self.camera_configs, config_file, indent=4)

    def update_source_matrix_vertical(self,new_val):
        self.source_matrix_depth_factor_v = float(new_val)

    def update_source_matrix_horizontal(self,new_val):
        self.source_matrix_depth_factor_h = float(new_val)

    def update_source_matrix_top_down(self,new_val):
        self.source_matrix_depth_factor_top_down = float(new_val)
        
    def update_destination_matrix_vertical(self,new_val):
        self.destination_matrix_depth_factor_v = float(new_val)

    def update_destination_matrix_horizontal(self,new_val):
        self.destination_matrix_depth_factor_h = float(new_val)

    def update_destination_matrix_top_down(self,new_val):
        self.destination_matrix_depth_factor_top_down = float(new_val)

    def update_wrapped_image_dimensions_vertical_h(self,new_val):
        self.wrapped_image_dimensions_vertical["h"] = int(float(new_val))

    def update_wrapped_image_dimensions_vertical_w(self,new_val):
        self.wrapped_image_dimensions_vertical['w'] = int(float(new_val))

    def update_wrapped_image_dimensions_horizontal_h(self,new_val):
        self.wrapped_image_dimensions_horizontal['h'] = int(float(new_val))

    def update_wrapped_image_dimensions_horizontal_w(self,new_val):
        self.wrapped_image_dimensions_horizontal['w'] = int(float(new_val))

    def update_wrapped_image_dimensions_top_down_h(self,new_val):
        self.wrapped_image_dimensions_top_down['h'] = int(float(new_val))

    def update_wrapped_image_dimensions_top_down_w(self,new_val):
        self.wrapped_image_dimensions_top_down['w'] = int(float(new_val))

    def update_front_camera_left_indentation(self,new_val):
        self.front_camera_left_indentation = float(new_val)
        self.pygame_images_window_placement['1'] = (self.pygame_window_dimensions['w']//self.front_camera_left_indentation, self.pygame_window_dimensions['h']//self.front_camera_top_indentation)

    def update_front_camera_top_indentation(self,new_val):
        self.front_camera_top_indentation = float(new_val)
        self.pygame_images_window_placement['1'] = (self.pygame_window_dimensions['w']//self.front_camera_left_indentation, self.pygame_window_dimensions['h']//self.front_camera_top_indentation)

    def update_right_camera_left_indentation(self,new_val):
        self.right_camera_left_indentation = float(new_val)
        self.pygame_images_window_placement['3'] = (self.pygame_window_dimensions['w']*2//self.right_camera_left_indentation, self.right_camera_top_indentation)

    def update_right_camera_top_indentation(self,new_val):
        self.right_camera_top_indentation = float(new_val)
        self.pygame_images_window_placement['3'] = (self.pygame_window_dimensions['w']*2//self.right_camera_left_indentation, self.right_camera_top_indentation)

    def update_rear_camera_left_indentation(self,new_val):
        self.rear_camera_left_indentation = float(new_val)
        self.pygame_images_window_placement['2'] = (self.pygame_window_dimensions['w']//self.rear_camera_left_indentation, self.pygame_window_dimensions['h']*2//self.rear_camera_top_indentation)

    def update_rear_camera_top_indentation(self,new_val):
        self.rear_camera_top_indentation = float(new_val)
        self.pygame_images_window_placement['2'] = (self.pygame_window_dimensions['w']//self.rear_camera_left_indentation, self.pygame_window_dimensions['h']*2//self.rear_camera_top_indentation)

    def update_left_camera_left_indentation(self,new_val):
        self.left_camera_left_indentation = float(new_val)
        self.pygame_images_window_placement['4'] = (self.left_camera_left_indentation, self.left_camera_top_indentation)

    def update_left_camera_top_indentation(self,new_val):
        self.left_camera_top_indentation = float(new_val)
        self.pygame_images_window_placement['4'] = (self.left_camera_left_indentation, self.left_camera_top_indentation)

CONFIG_MODIFICATIONS_INSTANCE = ConfigModifier.get_instance()
# Call the save_camera_configs function before program exit
atexit.register(CONFIG_MODIFICATIONS_INSTANCE.save_camera_configs)
