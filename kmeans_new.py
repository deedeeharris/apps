import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans

# Function to segment the image using K-Means clustering
def segment_image(image, n_clusters):
    # Convert the image to a 2D array of pixels
    pixels = image.reshape((image.shape[0] * image.shape[1], 3))

    # Apply K-Means clustering to the pixels
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(pixels)

    # Create a labeled mask by assigning each pixel to its cluster
    labels = kmeans.labels_.reshape(image.shape[:2])
    
    return labels

# Function to create a colored mask from a labeled mask
def create_mask(labels):
    # Create a mask image with the same dimensions as the input image
    mask = np.zeros_like(labels, dtype=np.uint8)

    # Assign a different color to each cluster
    for i in range(labels.max() + 1):
        mask[labels == i] = np.array([i, i, i])
    
    return mask

# Function to segment a specific object in the image based on the selected mask
def display_segmented_object(mask, image):
    # Convert the mask to grayscale
    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    
    # Threshold the mask to create a binary image
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    
    # Bitwise-and the image with the mask to extract the object
    object = cv2.bitwise_and(image, image, mask=threshold)
    
    # Display the segmented object using Streamlit
    st.image(object)

# Main function
def main():
    # Allow the user to upload an image
    image = st.file_uploader("Upload an image", type="jpg")
    
    # Check if an image was uploaded
    if image is not None:
        # Convert the image to a NumPy array
        image = np.frombuffer(image.read(), np.uint8)
        
        # Decode the image
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        
        # Segment the image using K-Means
        labels = segment_image(image, n_clusters=5)
        
        # Create a colored mask from the labeled mask
        mask = create_mask(labels)
        
        # Display the labeled mask
        st.image(mask)
        
        display_segmented_object(mask, image)

