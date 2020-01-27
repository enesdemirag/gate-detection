import cv2
import matplotlib.patches as patches
import matplotlib.pyplot as plt

import torch
import torchvision
import matplotlib.pyplot as plt

from torchvision import transforms

from detecto import core
from detecto import utils
from detecto import visualize

labels = ['gate']
model = core.Model.load('trained_model.pth', labels)

input_file = 'test.mp4'
output_file = 'output.avi'

fps=30

# Read in the video
video = cv2.VideoCapture(input_file)

# Video frame dimensions
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Scale down frames when passing into model for faster speeds
scaled_size = 800
scale_down_factor = min(frame_height, frame_width) / scaled_size

# The VideoWriter with which we'll write our video with the boxes and labels
# Parameters: filename, fourcc, fps, frame_size
out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'DIVX'), fps, (frame_width, frame_height))

# Transform to apply on individual frames of the video
transform_frame = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(scaled_size),
    transforms.ToTensor(),
    utils.normalize_transform(),
])

# Loop through every frame of the video
while True:
    ret, frame = video.read()
    # Stop the loop when we're done with the video
    if not ret:
        break

    # The transformed frame is what we'll feed into our model
    transformed_frame = transform_frame(frame)
    predictions = model.predict_top(transformed_frame)

    # Add the top prediction of each class to the frame
    for label, box, score in zip(*predictions):
        # Since the predictions are for scaled down frames,
        # we need to increase the box dimensions
        box *= scale_down_factor
        # Create the box around each object detected
        # Parameters: frame, (start_x, start_y), (end_x, end_y), (r, g, b), thickness
        if round(score.item(), 2) > 0.8:
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 3)
            # Write the label and score for the boxes
            # Parameters: frame, text, (start_x, start_y), font, font scale, (r, g, b), thickness
            cv2.putText(frame, '{}: {}'.format(label, round(score.item(), 2)), (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    # Write this frame to our video file
    out.write(frame)
    print('next frame')
    # If the 'q' key is pressed, break from the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# When finished, release the video capture and writer objects
video.release()
out.release()

# Close all the frames
cv2.destroyAllWindows()
