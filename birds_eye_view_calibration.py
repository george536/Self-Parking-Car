import tkinter as tk
from camera_config import *
import camera_config as cam_cnf

def update_source_matrix(new_val):
    cam_cnf.source_matrix_depth_factor = float(new_val)
    
def update_destination_matrix(new_val):
    cam_cnf.destination_matrix_depth_factor = float(new_val)

def update_wrapped_image_dimensions_vertical_h(new_val):
    cam_cnf.wrapped_image_dimensions_vertical['h'] = int(new_val)

def update_wrapped_image_dimensions_vertical_w(new_val):
    cam_cnf.wrapped_image_dimensions_vertical['w'] = int(new_val)

def update_wrapped_image_dimensions_horizontal_h(new_val):
    cam_cnf.wrapped_image_dimensions_horizontal['h'] = int(new_val)

def update_wrapped_image_dimensions_horizontal_w(new_val):
    cam_cnf.wrapped_image_dimensions_horizontal['w'] = int(new_val)

def update_front_camera_left_indentation(new_val):
    cam_cnf.front_camera_left_indentation = float(new_val)
    cam_cnf.pygame_images_window_placement['1'] = (cam_cnf.pygame_window_dimensions['w']//cam_cnf.front_camera_left_indentation, cam_cnf.pygame_window_dimensions['h']//cam_cnf.front_camera_top_indentation)

def update_front_camera_top_indentation(new_val):
    cam_cnf.front_camera_top_indentation = float(new_val)
    cam_cnf.pygame_images_window_placement['1'] = (cam_cnf.pygame_window_dimensions['w']//cam_cnf.front_camera_left_indentation, cam_cnf.pygame_window_dimensions['h']//cam_cnf.front_camera_top_indentation)

def update_right_camera_left_indentation(new_val):
    cam_cnf.right_camera_left_indentation = float(new_val)
    cam_cnf.pygame_images_window_placement['2'] = (cam_cnf.pygame_window_dimensions['w']*2//cam_cnf.right_camera_left_indentation, 0)

def update_rear_camera_left_indentation(new_val):
    cam_cnf.rear_camera_left_indentation = float(new_val)
    cam_cnf.pygame_images_window_placement['3'] = (cam_cnf.pygame_window_dimensions['w']//cam_cnf.rear_camera_left_indentation, cam_cnf.pygame_window_dimensions['h']*2//cam_cnf.rear_camera_top_indentation)

def update_rear_camera_top_indentation(new_val):
    cam_cnf.rear_camera_top_indentation = float(new_val)
    cam_cnf.pygame_images_window_placement['3'] = (cam_cnf.pygame_window_dimensions['w']//cam_cnf.rear_camera_left_indentation, cam_cnf.pygame_window_dimensions['h']*2//cam_cnf.rear_camera_top_indentation)

class BIVCalibration:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bird's Eye View Calibration")
        self.root.resizable(True, True)

        # source matrix vars
        self.source_matrix_depth_factor = tk.DoubleVar()
        self.source_matrix_depth_factor_slider = tk.Scale(self.root, from_=0, to = 10, length = 500, resolution = 0.1, variable = self.source_matrix_depth_factor, label = "source_matrix_depth_factor", command = update_source_matrix, orient = "horizontal")
        self.source_matrix_depth_factor_slider.set(source_matrix_depth_factor)
        self.source_matrix_depth_factor_slider.pack()

        # destination matrix vars
        self.destination_matrix_depth_factor = tk.DoubleVar()
        self.destination_matrix_depth_factor_slider = tk.Scale(self.root, from_=0, to = 100, length = 500, resolution = 0.1, variable = self.destination_matrix_depth_factor, label = "destination_matrix_depth_factor", command = update_destination_matrix, orient = "horizontal")
        self.destination_matrix_depth_factor_slider.set(destination_matrix_depth_factor)
        self.destination_matrix_depth_factor_slider.pack()

        # scaled size vertical
        self.wrapped_image_dimensions_vertical_h = tk.DoubleVar()
        self.wrapped_image_dimensions_vertical_h_slider = tk.Scale(self.root, from_=0, to = 2000, length = 500, resolution = 1, variable = self.wrapped_image_dimensions_vertical_h, label = "wrapped_image_dimensions_vertical_h", command = update_wrapped_image_dimensions_vertical_h, orient = "horizontal")
        self.wrapped_image_dimensions_vertical_h_slider.set(wrapped_image_dimensions_vertical['h'])
        self.wrapped_image_dimensions_vertical_h_slider.pack()

        self.wrapped_image_dimensions_vertical_w = tk.DoubleVar()
        self.wrapped_image_dimensions_vertical_w_slider = tk.Scale(self.root, from_=0, to = 2000, length = 500, resolution = 1, variable = self.wrapped_image_dimensions_vertical_w, label = "wrapped_image_dimensions_vertical_w", command = update_wrapped_image_dimensions_vertical_w, orient = "horizontal")
        self.wrapped_image_dimensions_vertical_w_slider.set(wrapped_image_dimensions_vertical['w'])
        self.wrapped_image_dimensions_vertical_w_slider.pack()

        # scaled size horizontal
        self.wrapped_image_dimensions_horizontal_h = tk.DoubleVar()
        self.wrapped_image_dimensions_horizontal_h_slider = tk.Scale(self.root, from_=0, to = 2000, length = 500, resolution = 1, variable = self.wrapped_image_dimensions_horizontal_h, label = "wrapped_image_dimensions_horizontal_h", command = update_wrapped_image_dimensions_horizontal_h, orient = "horizontal")
        self.wrapped_image_dimensions_horizontal_h_slider.set(wrapped_image_dimensions_horizontal['h'])
        self.wrapped_image_dimensions_horizontal_h_slider.pack()

        self.wrapped_image_dimensions_horizontal_w = tk.DoubleVar()
        self.wrapped_image_dimensions_horizontal_w_slider = tk.Scale(self.root, from_=0, to = 2000, length = 500, resolution = 1, variable = self.wrapped_image_dimensions_horizontal_w, label = "wrapped_image_dimensions_horizontal_w", command = update_wrapped_image_dimensions_horizontal_w, orient = "horizontal")
        self.wrapped_image_dimensions_horizontal_w_slider.set(wrapped_image_dimensions_horizontal['w'])
        self.wrapped_image_dimensions_horizontal_w_slider.pack()

        # image loc 1
        self.front_camera_left_indentation_var = tk.DoubleVar()
        self.front_camera_left_indentation_slider = tk.Scale(self.root, from_=0.01, to = 50, length = 500, resolution = 0.1, variable = self.front_camera_left_indentation_var, label = "front_camera_left_indentation", command = update_front_camera_left_indentation, orient = "horizontal")
        self.front_camera_left_indentation_slider.set(front_camera_left_indentation)
        self.front_camera_left_indentation_slider.pack()

        self.front_camera_top_indentation_var = tk.DoubleVar()
        self.front_camera_top_indentation_slider = tk.Scale(self.root, from_=0.01, to = 50, length = 500, resolution = 0.1, variable = self.front_camera_top_indentation_var, label = "front_camera_top_indentation", command = update_front_camera_top_indentation, orient = "horizontal")
        self.front_camera_top_indentation_slider.set(front_camera_top_indentation)
        self.front_camera_top_indentation_slider.pack()

        # image loc 2
        self.right_camera_left_indentation_var = tk.DoubleVar()
        self.right_camera_left_indentation_slider = tk.Scale(self.root, from_=0.01, to = 50, length = 500, resolution = 0.1, variable = self.right_camera_left_indentation_var, label = "right_camera_left_indentation", command = update_right_camera_left_indentation, orient = "horizontal")
        self.right_camera_left_indentation_slider.set(right_camera_left_indentation)
        self.right_camera_left_indentation_slider.pack()

        # image loc 3
        self.rear_camera_left_indentation_var = tk.DoubleVar()
        self.rear_camera_left_indentation_slider = tk.Scale(self.root, from_=0.01, to = 50, length = 500, resolution = 0.1, variable = self.rear_camera_left_indentation_var, label = "rear_camera_left_indentation", command = update_rear_camera_left_indentation, orient = "horizontal")
        self.rear_camera_left_indentation_slider.set(rear_camera_left_indentation)
        self.rear_camera_left_indentation_slider.pack()

        self.rear_camera_top_indentation_var = tk.DoubleVar()
        self.rear_camera_top_indentation_slider = tk.Scale(self.root, from_=0.01, to = 50, length = 500, resolution = 0.1, variable = self.rear_camera_top_indentation_var, label = "rear_camera_top_indentation", command = update_rear_camera_top_indentation, orient = "horizontal")
        self.rear_camera_top_indentation_slider.set(rear_camera_top_indentation)
        self.rear_camera_top_indentation_slider.pack()

        self.root.mainloop()