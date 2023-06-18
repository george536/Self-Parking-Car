import tkinter as tk
from Birds_Eye_View.camera_configs_modifier import *
from threading import Thread

class BEVCalibration(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.root = tk.Tk()
        self.root.title("Bird's Eye View Calibration")
        self.root.resizable(True, True)
        config_modifications_insatnce = ConfigModifier.get_instance()
        
        sliders = [
            ("source_matrix_depth_factor_vertical", config_modifications_insatnce.source_matrix_depth_factor_v, config_modifications_insatnce.update_source_matrix_vertical, 0.1, 25, 0.1),
            ("source_matrix_depth_factor_horizontal", config_modifications_insatnce.source_matrix_depth_factor_h, config_modifications_insatnce.update_source_matrix_horizontal, 0.1, 25, 0.1),
            ("destination_matrix_depth_factor_vertical", config_modifications_insatnce.destination_matrix_depth_factor_v, config_modifications_insatnce.update_destination_matrix_vertical, 1, 100, 0.1),
            ("destination_matrix_depth_factor_horizontal", config_modifications_insatnce.destination_matrix_depth_factor_h, config_modifications_insatnce.update_destination_matrix_horizontal, 1, 50, 0.1),
            ("wrapped_image_dimensions_vertical_h", config_modifications_insatnce.wrapped_image_dimensions_vertical['h'], config_modifications_insatnce.update_wrapped_image_dimensions_vertical_h, 1, 1000, 1),
            ("wrapped_image_dimensions_vertical_w", config_modifications_insatnce.wrapped_image_dimensions_vertical['w'], config_modifications_insatnce.update_wrapped_image_dimensions_vertical_w, 1, 1000, 1),
            ("wrapped_image_dimensions_horizontal_h", config_modifications_insatnce.wrapped_image_dimensions_horizontal['h'], config_modifications_insatnce.update_wrapped_image_dimensions_horizontal_h, 1, 1000, 1),
            ("wrapped_image_dimensions_horizontal_w", config_modifications_insatnce.wrapped_image_dimensions_horizontal['w'], config_modifications_insatnce.update_wrapped_image_dimensions_horizontal_w, 1, 1000, 10),
            ("front_camera_left_indentation", config_modifications_insatnce.front_camera_left_indentation, config_modifications_insatnce.update_front_camera_left_indentation, 0, 50, 0.1),
            ("front_camera_top_indentation", config_modifications_insatnce.front_camera_top_indentation, config_modifications_insatnce.update_front_camera_top_indentation, 0, 50, 0.1),
            ("right_camera_left_indentation", config_modifications_insatnce.right_camera_left_indentation, config_modifications_insatnce.update_right_camera_left_indentation, 0, 50, 0.1),
            ("right_camera_top_indentation", config_modifications_insatnce.right_camera_top_indentation, config_modifications_insatnce.update_right_camera_top_indentation, -50, 50, 0.1),
            ("rear_camera_left_indentation", config_modifications_insatnce.rear_camera_left_indentation, config_modifications_insatnce.update_rear_camera_left_indentation, 0, 50, 0.1),
            ("rear_camera_top_indentation", config_modifications_insatnce.rear_camera_top_indentation, config_modifications_insatnce.update_rear_camera_top_indentation, 0, 50, 0.1),
            ("left_camera_left_indentation", config_modifications_insatnce.left_camera_left_indentation, config_modifications_insatnce.update_left_camera_left_indentation, 0, 50, 0.1),
            ("left_camera_top_indentation", config_modifications_insatnce.left_camera_top_indentation, config_modifications_insatnce.update_left_camera_top_indentation, -50, 50, 0.1)
        ]

        for i, (label, value, command, from_val, to_val, step) in enumerate(sliders):
            var = tk.DoubleVar(value=value)
            slider = tk.Scale(
                self.root,
                from_=from_val,
                to=to_val,
                length=500,
                resolution=step,
                variable=var,
                label=label,
                command=command,
                orient="horizontal"
            )
            slider.set(value)
            slider.grid(row=i//2, column=i%2)
        
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.root.mainloop()

