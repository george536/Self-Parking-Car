import os
import cv2
from torch.utils.data import Dataset
import os
import cv2
import albumentations as A
from torch.utils.data import Dataset
from ml_io.parking_spot_image import ParkingSpotImage

class ParkingDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.image_files = os.listdir(root_dir)
        self.filter_image_files()
        
        self.parking_spot_images = []
        self.populate_parking_spots()
        
        
        self.parking_spots = []
        self.load_parking_spots()
        
        self.transform = transform
        
    def match_images_to_spots(self):
        pass    
    
    def populate_parking_spots(self):
        for image_file in self.image_files:
            parking_spot = ParkingSpotImage(image_file)  # Assuming ParkingSpot class takes image_file as argument
            self.parking_spot_images.append(parking_spot)
        
    def filter_image_files(self):
        self.image_files = [os.path.join(self.root_dir, f) for f in self.image_files if f.endswith('.jpg') or f.endswith('.png')]
        
    def load_parking_spots(self):
        pass

    def __len__(self):
        return len(self.parking_spot_images)

    def __getitem__(self, idx):
        
        image_parking_spot = self.parking_spot_images[idx].get_image()
        
        if self.transform:
            image = self.transform(image=image_parking_spot)["image"]
        
        return image
    
    
    



if __name__ == "__main__":

    # Usage example:
    transform = A.Compose([
        A.ToTensorV2()
    ])

    dataset = ParkingDataset('/test_images', transform=transform)
    image = dataset[0]  # Load the first image lazily and apply transformations