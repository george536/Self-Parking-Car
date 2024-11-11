import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, SubsetRandomSampler
from torchvision import models
from ml.ml_io.dataset_loader import DatasetLoader
import numpy as np
import cv2
import albumentations as A

transform_train = A.Compose([
    A.ISONoise(p=0.3),
    A.Blur(blur_limit=2,p=0.2),
    A.HueSaturationValue(p=0.3),
    A.ToTensorV2(),
])

transform_val = A.Compose([
    A.ToTensorV2()
])

batch_size = 4
images_directory_path = "D:\CARLA_0.9.14\Self-Parking-Car\training_data"
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

class ResNet50ParkingSpotDetector(nn.Module):
    def __init__(self, max_spots=10):
        super(ResNet50ParkingSpotDetector, self).__init__()
        self.resnet50 = models.resnet50(pretrained=True)

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
        x = torch.flatten(x, 1) # Flatten to [batch_size, 1024]

        # Classification
        cls_logits = self.classifier(x)
        cls_logits = cls_logits.view(-1, self.max_spots)
        # Regression
        bbox_reg = self.regressor(x)
        bbox_reg = bbox_reg.view(-1, self.max_spots, 8)
        return bbox_reg, cls_logits

model = ResNet50ParkingSpotDetector()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Loss and optimizer
def custom_loss(predictions, targets):
    mask = targets[..., -1] != -1
    loss = ((predictions - targets) ** 2) * mask.unsqueeze(-1).expand_as(predictions)
    return loss.mean()

optimizer = optim.Adam(model.parameters(), lr=1e-4)

# Training loop
num_epochs = 25
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = custom_loss(outputs, labels)
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
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            loss = custom_loss(outputs, labels)
            val_loss += loss.item() * images.size(0)

    val_loss /= len(val_loader.dataset)
    print(f'Validation Loss: {val_loss:.4f}')

# Inference
def predict_parking_spots(image):
    model.eval()
    with torch.no_grad():
        image = transform(image).unsqueeze(0).to(device)
        outputs = model(image).cpu().numpy().reshape(-1, 8)
        predicted_coordinates = [coords for coords in outputs if coords[-1] != -1]  # Filter out padded values
        return np.array(predicted_coordinates)

# Load an example image and predict
example_image = cv2.imread('example.jpg')
predicted_coordinates = predict_parking_spots(example_image)
print(predicted_coordinates)