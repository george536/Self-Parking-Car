from ml.ml_io.transform import Transform

class ParkingSpot:
    def __init__(self, spot_id, x_BL, y_BL, x_UL, y_UL, x_UR, y_UR, x_BR, y_BR):
        self.spot_id = spot_id
        self.x_BL = x_BL
        self.y_BL = y_BL
        self.x_UL = x_UL
        self.y_UL = y_UL
        self.x_UR = x_UR
        self.y_UR = y_UR
        self.x_BR = x_BR
        self.y_BR = y_BR

    def get_spot_id(self):
        return self.spot_id
    
    def get_relative_corners_transform_to_car(self, car_transform: Transform):
        x_BL = self.x_BL - car_transform.x
        y_BL = self.y_BL - car_transform.y
        x_UL = self.x_UL - car_transform.x
        y_UL = self.y_UL - car_transform.y
        x_UR = self.x_UR - car_transform.x
        y_UR = self.y_UR - car_transform.y
        x_BR = self.x_BR - car_transform.x
        y_BR = self.y_BR - car_transform.y

        return [1.0, x_BL, y_BL, x_UL, y_UL, x_UR, y_UR, x_BR, y_BR]