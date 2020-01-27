import torch
import torchvision
import matplotlib.pyplot as plt

from torchvision import transforms

from detecto import core
from detecto import utils
from detecto import visualize

# Specify a list of transformations for our dataset to apply on our images
transform_img = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(800),
    transforms.RandomHorizontalFlip(0.5),
    transforms.ToTensor(),
    utils.normalize_transform(),])

dataset = core.Dataset('train_labels.csv', 'images/', transform=transform_img)

# Create our validation dataset
val_dataset = core.Dataset('test_labels.csv', 'images/', transform=transform_img)

# Create the loaders for our train and validation datasets
loader = core.DataLoader(dataset, batch_size=2, shuffle=True)
val_loader = core.DataLoader(val_dataset)

# Create our model, passing in all unique classes we're predicting
# Note: make sure these match exactly with the labels in the XML/CSV files!
model = core.Model(['gate'])

# Train the model! This step can take a while, so make sure you
# the GPU is turned on in Edit -> Notebook settings
losses = model.fit(loader, val_loader, epochs=30, learning_rate=0.01, gamma=0.2, lr_step_size=5, verbose=True)

model.save('trained_model.pth')