import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, SubsetRandomSampler
from torchvision import models
from ml.ml_io.dataset_loader import DatasetLoader
import numpy as np
import cv2
import albumentations as A
from albumentations.pytorch import ToTensorV2
from ml.model_train.model import ResNet50ParkingSpotDetector

transform_train = A.Compose([
    A.ISONoise(p=0.3),
    A.Blur(blur_limit=2,p=0.2),
    A.HueSaturationValue(p=0.3),
    ToTensorV2(),
])

transform_val = A.Compose([
    ToTensorV2()
])

batch_size = 4
images_directory_path = "D:\\CARLA_0.9.14\\Self-Parking-Car\\training_data"
train_data = DatasetLoader(images_directory_path,transform=transform_train)
val_data = DatasetLoader (images_directory_path, transform=transform_val)

num_elements = len(train_data)
indices = list(range(num_elements))
np.random.shuffle(indices)

val_split_index = int(np.floor(0.2*num_elements))
train_idx, val_idx = indices[val_split_index:], indices[:val_split_index]

train_sampler = SubsetRandomSampler(train_idx)
val_sampler = SubsetRandomSampler(val_idx)

train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True, num_workers=24, pin_memory=True, sampler=train_sampler)
val_loader = DataLoader(val_data, batch_size=batch_size, shuffle=False, num_workers=24, pin_memory=True, sampler=val_sampler)


model = ResNet50ParkingSpotDetector()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Loss and optimizer
def custom_loss(predictions, targets):
     # Unpack predictions
    pred_boxes, pred_conf = predictions  # pred_boxes: [batch_size, max_spots, 8], pred_conf: [batch_size, max_spots]

    # Unpack targets
    target_boxes, target_conf = targets  # target_boxes: [batch_size, max_spots, 8], target_conf: [batch_size, max_spots]

    # Ensure targets are on the same device as predictions
    device = pred_boxes.device
    target_boxes = target_boxes.to(device)
    target_conf = target_conf.to(device)

    # Create a mask for valid spots (where target_conf == 1)
    mask = target_conf == 1  # Shape: [batch_size, max_spots]

    # Compute Regression Loss (Smooth L1 Loss) for valid spots
    if mask.any():
        # Only compute loss where mask is True
        pred_boxes_valid = pred_boxes[mask]
        target_boxes_valid = target_boxes[mask]
        loc_loss = F.smooth_l1_loss(pred_boxes_valid, target_boxes_valid)
    else:
        # If no valid spots, set loc_loss to zero
        loc_loss = torch.tensor(0.0, device=device)

    # Compute Classification Loss (Binary Cross-Entropy Loss)
    conf_loss = F.binary_cross_entropy(pred_conf, target_conf.float())

    # Total Loss
    total_loss = loc_loss + conf_loss
    return total_loss

optimizer = optim.Adam(model.parameters(), lr=1e-4)

def train():

    # Training loop
    num_epochs = 25
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for images, labels in train_loader:

            images = images.to(device)

            target_boxes, target_conf = labels

            # Move targets to the device
            target_boxes = target_boxes.to(device)
            target_conf = target_conf.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = custom_loss(outputs, (target_boxes, target_conf))
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)

        epoch_loss = running_loss / len(train_loader.dataset)
        print(f'Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}')

        # Validation loop
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for images, labels in val_loader:
                
                val_images = images.to(device)

                val_target_boxes, val_target_conf = labels

                # Move targets to the device
                val_target_boxes = val_target_boxes.to(device)
                val_target_conf = val_target_conf.to(device)

                val_outputs = model(val_images)
                val_loss = custom_loss(val_outputs, (val_target_boxes, val_target_conf))
                val_loss += loss.item() * images.size(0)

        val_loss /= len(val_loader.dataset)
        print(f'Validation Loss: {val_loss:.4f}')



if __name__ == "__main__":
