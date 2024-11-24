import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset
from torchvision import models
from ml.ml_io.parking_spot_image import ParkingSpotImage
from ml.database.model_database_provider import ModelDatabaseProvider
from ml.ml_io.parking_spot import ParkingSpot
from ml.ml_io.transform import Transform
import albumentations as A
from albumentations.pytorch import ToTensorV2


import cv2

class ResNet50ParkingSpotDetector(nn.Module):
    def __init__(self, max_spots=10):
        super(ResNet50ParkingSpotDetector, self).__init__()
        self.resnet50 = models.resnet50(pretrained=True)

        self.max_spots = max_spots

        # Remove the last fully connected layer
        self.features = nn.Sequential(*list(self.resnet50.children())[:-2])  # Exclude avgpool and fc

        self.conv = nn.Sequential(
            nn.Conv2d(2048, 1024, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
        )

        # Adaptive pooling layer
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))

        # Classification head
        self.classifier = nn.Sequential(
            nn.Conv2d(1024, self.max_spots, kernel_size=1),
            nn.Sigmoid(),  # Outputs confidence scores between 0 and 1
        )
        
        # Regression head
        # Output 8 coordinates per spot
        self.regressor = nn.Conv2d(1024, self.max_spots * 8, kernel_size=1)
        

    def forward(self, x):
        x = self.features(x)    # Extract features
        x = self.conv(x)        # Additional processing
        x = self.avgpool(x)     # Reduce spatial dimensions to 1x1
       # x = torch.flatten(x, 1) # Flatten to [batch_size, 1024]

        # Classification
        cls_logits = self.classifier(x)
        cls_logits = cls_logits.view(-1, self.max_spots)
        # Regression
        bbox_reg = self.regressor(x)
        bbox_reg = bbox_reg.view(-1, self.max_spots, 8)
        return bbox_reg, cls_logits



if __name__ == "__main__":

    model = ResNet50ParkingSpotDetector(max_spots=10)

    transform_val = A.Compose([
    ToTensorV2()
    ])

    model.eval()

    image = cv2.imread('8.jpg')

    device = "cuda"
    output = None

    model.to(device)

    with torch.no_grad():
        image = transform_val(image = image)["image"].float().unsqueeze(0).to(device)
        bbox_reg, cls_logits = model(image)

        # Move tensors to CPU and convert to NumPy arrays
        bbox_reg = bbox_reg.cpu().numpy().reshape(-1, 8)
        cls_logits = cls_logits.cpu().numpy().reshape(-1)

        print(bbox_reg)
        print(cls_logits)

