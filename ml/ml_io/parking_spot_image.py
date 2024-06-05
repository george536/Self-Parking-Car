import cv2
from ml.ml_io.parking_spot import ParkingSpot
from ml.ml_io.transform import Transform

class ParkingSpotImage:
    def __init__(self, image_path, transform: Transform = None):
        self.image_path = image_path
        self.transform = transform
        self.parking_spots = []

    def get_image(self):
        image = cv2.imread(self.image_path)
        return image

    def add_parking_spot(self, spot: ParkingSpot):
        self.parking_spots.append(spot)

    def get_parking_spots(self):
        return self.parking_spots
    
    def get_parking_spots_labels(self):
        spots_labels = []
        for i in range(10):
            if i < len(self.parking_spots):
                spots_labels += self.parking_spots[i].get_relative_corners_transform_to_car(self.transform)
            else:
                spots_labels += [0.0] * 9