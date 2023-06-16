import tkinter as tk
import camera_configs_manager as cam_cnf

class BIVCalibration:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bird's Eye View Calibration")
        self.root.resizable(True, True)
        
        sliders = [
            ("source_matrix_depth_factor_vertical", cam_cnf.source_matrix_depth_factor_v, cam_cnf.update_source_matrix_vertical, 0.1, 5, 0.1),
            ("source_matrix_depth_factor_horizontal", cam_cnf.source_matrix_depth_factor_h, cam_cnf.update_source_matrix_horizontal, 0.1, 5, 0.1),
            ("destination_matrix_depth_factor_vertical", cam_cnf.destination_matrix_depth_factor_v, cam_cnf.update_destination_matrix_vertical, 1, 50, 1),
            ("destination_matrix_depth_factor_horizontal", cam_cnf.destination_matrix_depth_factor_h, cam_cnf.update_destination_matrix_horizontal, 1, 50, 1),
            ("wrapped_image_dimensions_vertical_h", cam_cnf.wrapped_image_dimensions_vertical['h'], cam_cnf.update_wrapped_image_dimensions_vertical_h, 100, 300, 10),
            ("wrapped_image_dimensions_vertical_w", cam_cnf.wrapped_image_dimensions_vertical['w'], cam_cnf.update_wrapped_image_dimensions_vertical_w, 200, 600, 10),
            ("wrapped_image_dimensions_horizontal_h", cam_cnf.wrapped_image_dimensions_horizontal['h'], cam_cnf.update_wrapped_image_dimensions_horizontal_h, 150, 350, 10),
            ("wrapped_image_dimensions_horizontal_w", cam_cnf.wrapped_image_dimensions_horizontal['w'], cam_cnf.update_wrapped_image_dimensions_horizontal_w, 300, 700, 10),
            ("front_camera_left_indentation", cam_cnf.front_camera_left_indentation, cam_cnf.update_front_camera_left_indentation, 0, 10, 0.5),
            ("front_camera_top_indentation", cam_cnf.front_camera_top_indentation, cam_cnf.update_front_camera_top_indentation, 0, 50, 1),
            ("right_camera_left_indentation", cam_cnf.right_camera_left_indentation, cam_cnf.update_right_camera_left_indentation, 0, 10, 0.5),
            ("right_camera_top_indentation", cam_cnf.right_camera_top_indentation, cam_cnf.update_right_camera_top_indentation, 0, 10, 0.5),
            ("rear_camera_left_indentation", cam_cnf.rear_camera_left_indentation, cam_cnf.update_rear_camera_left_indentation, 0, 10, 0.5),
            ("rear_camera_top_indentation", cam_cnf.rear_camera_top_indentation, cam_cnf.update_rear_camera_top_indentation, 0, 10, 0.5),
            ("left_camera_left_indentation", cam_cnf.left_camera_left_indentation, cam_cnf.update_left_camera_left_indentation, 0, 10, 0.5),
            ("left_camera_top_indentation", cam_cnf.left_camera_top_indentation, cam_cnf.update_left_camera_top_indentation, 0, 10, 0.5)
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

