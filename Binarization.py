import cv2
import numpy as np
from tkinter import filedialog

file_path = filedialog.askopenfilename()

if file_path:
    image = cv2.imread(file_path)

# Define a function to get the binary image
def get_binary_image(image, threshold):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow('Binary Image', binary)
    # cv2.imshow('gray Image', gray)
    return binary

# Define a function to get the percentage of black area in the binary image
def get_black_area_percentage(binary_image):
    black_pixels = np.sum(binary_image == 0)
    total_pixels = binary_image.shape[0] * binary_image.shape[1]
    percentage = (black_pixels / total_pixels) * 100
    return percentage

# # Define a callback function for the trackbar
def on_trackbar(val):
    binary_image = get_binary_image(image, val)
    binary_image_3c = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
    binary_image_3c[np.where((binary_image_3c == [255, 255, 255]).all(axis=2))] = [0, 0, 0]
    alpha = 0.5
    output = cv2.addWeighted(image, 1 - alpha, binary_image_3c, alpha, 0)
    black_area_percentage = get_black_area_percentage(binary_image)
    cv2.putText(output, f'Eutectoid fraction percentage: {black_area_percentage:.2f}%', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Output', output)


# # Load the original image in JPG format
# image = cv2.imread('test.jpg')

# Create a window to display the output
cv2.namedWindow('Output')

# Create a trackbar to adjust the threshold value
cv2.createTrackbar('Threshold', 'Output', 0, 255, on_trackbar)

# Display the output for the initial threshold value
on_trackbar(0)

# Wait for a key event and then exit
cv2.waitKey(0)
cv2.destroyAllWindows()

