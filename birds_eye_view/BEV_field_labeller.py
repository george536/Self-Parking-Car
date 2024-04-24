import numpy as np
from parking_spot_labeller.utils_labeller import draw_bounding_box
from carla import Color

class BEVFieldLabeller:
    def __init__(self, world, vehicle, should_show_bev_filed_box):
        self.upper_left_corner_shifts = [-7,4.6]
        self.upper_right_corner_shifts = [7,4.6]
        self.lower_left_corner_shifts = [-7,-4.6]
        self.lower_right_corner_shifts = [7,-4.6]
        self.shifted_rotated_points = []
        self.world = world
        self.vehicle = vehicle
        self.should_show_bev_filed_box = should_show_bev_filed_box
        self.calculate_field_corners()

    def calculate_field_corners(self):
        # rotate the shifting box
        angle = np.radians(self.vehicle.get_transform().rotation.yaw)
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                     [np.sin(angle), np.cos(angle)]])

        corner_shifts = [self.lower_left_corner_shifts,
                    self.upper_left_corner_shifts,
                    self.upper_right_corner_shifts,
                    self.lower_right_corner_shifts]

        rotated_shift_points = [np.dot(rotation_matrix, np.array(p)) for p in corner_shifts]
        rotated_shift_points = [(p[0], p[1], 0.2) for p in rotated_shift_points]

        car_location = [self.vehicle.get_transform().location.x, 
                        self.vehicle.get_transform().location.y, 
                        self.vehicle.get_transform().location.z]
        
        # apply the shift amounts to car location (the center of the box)
        self.shifted_rotated_points = []
        for shifted_point in rotated_shift_points:
            new_rotated_point = []
            new_rotated_point.append(shifted_point[0] + car_location[0])
            new_rotated_point.append(shifted_point[1] + car_location[1])
            new_rotated_point.append(car_location[2])
            self.shifted_rotated_points.append(new_rotated_point)

    def draw_field_box(self):
        draw_bounding_box(self.world, self.shifted_rotated_points, Color(0, 255, 0), 0.5)
        
    def update_box(self):
        self.calculate_field_corners()
        if self.should_show_bev_filed_box:
            self.draw_field_box()

    def get_field_box_points(self):
        """ order of points: left bottom -> left top -> right top -> right bottom """
        return self.shifted_rotated_points