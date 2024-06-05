import os
import torch
from torch.utils.data import Dataset
from ml_io.parking_spot_image import ParkingSpotImage
from ml.database.model_database_provider import ModelDatabaseProvider
from ml.ml_io.parking_spot import ParkingSpot
from ml.ml_io.transform import Transform

class DatasetLoader(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform

        self.image_ids = []
    
        self.parking_spot_images = []
        self.populate_parking_spots()

        self.match_images_to_spots()

    def populate_parking_spots(self):
        db_provider = ModelDatabaseProvider()

        self.image_ids = db_provider.get_all_image_ids()
        for image_id in self.image_ids:
            image_path = os.path.join(self.root_dir, str(image_id)) + ('.jpg')
            parking_spot_image = ParkingSpotImage(image_path, Transform(db_provider.get_car_transform(image_id)))
            self.parking_spot_images.append(parking_spot_image)

        db_provider.close() 

    def match_images_to_spots(self):
        db_provider = ModelDatabaseProvider()

        for parking_spot_image in self.parking_spot_images:
            image_id = int(os.path.splitext(os.path.basename(parking_spot_image.image_path))[0])
            in_view_spots = db_provider.get_all_in_view_spots(image_id)
            
            for spot_id in in_view_spots:
                spot_details = db_provider.get_parking_spot_corners(int(spot_id))
                if spot_details:
                    spot = ParkingSpot(int(spot_id), *spot_details)
                    parking_spot_image.add_parking_spot(spot)
        
        db_provider.close()   

    def __len__(self):
        return len(self.parking_spot_images)

    def __getitem__(self, idx):
        image_parking_spot = self.parking_spot_images[idx].get_image()
        
        if self.transform:
            image = self.transform(image=image_parking_spot)["image"]
        
        return image, torch.Tensor(image.get_parking_spots_labels())