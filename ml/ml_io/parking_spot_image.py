import dataset_loader
import transform
import cv2

class ParkingSpotImage:
    def __init__(self, image_path, transform=None):
        self.image_path = image_path
        self.transform = transform
        self.parking_spots = []
        
    def get_image(self):
        image = cv2.imread(self.image_path)
        return image

    def add_parking_spot(self, spot):
        self.parking_spots.append(spot)

    def get_parking_spots(self):
        return self.parking_spots