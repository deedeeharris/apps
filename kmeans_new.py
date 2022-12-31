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

    # Assign a different color to each cluster using the color map
    for i in range(256):
        mask[labels == i] = i
    
    return mask



# Function to segment a specific object in the image based on the selected mask
def display_segmented_object(mask, image):
    # Check if the mask is a 2D or 3D array
    if mask.ndim == 2:
        # Create a new image from the 2D mask array
        mask_image = cv2.merge((mask, mask, mask))
    elif mask.ndim == 3:
        # Create a new image from the 3D mask array
        mask_image = cv2.merge((mask[:,:,0], mask[:,:,1], mask[:,:,2]))
    else:
        # Raise an error if the mask is not a 2D or 3D array
        raise ValueError("Invalid mask array")
    
    # Convert the colored mask to grayscale
    gray = cv2.cvtColor(mask_image, cv2.COLOR_BGR2GRAY)
    
    # Threshold the mask to create a binary image
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    
    # Bitwise-and the image with the mask to extract the object
    object = cv2.bitwise_and(image, image, mask=threshold)
    
    # Display a "Please wait" message
    st.markdown("Please wait...")
    
    # Display the segmented object using Streamlit
    st.image(object)
    
    # Clear the "Please wait" message
    st.markdown("")


def select_object(mask, image):
    blank_image = np.zeros_like(image)
    labels = np.unique(mask)
    #color_map = np.random.randint(0, 256, (len(labels), 3), dtype=np.uint8)
    colored_mask = np.zeros_like(mask)
    for i in labels:
        colored_mask[mask == i] = i
    colored_mask_image = cv2.cvtColor(colored_mask, cv2.COLOR_GRAY2BGR)
    click_data = st.image(colored_mask_image, use_column_width=True)
    if click_data is not None:
        try:
            x, y = click_data["points"][0]
        except (KeyError, IndexError):
            # Handle the exception here
            return
        label = mask[y, x]
        object = cv2.bitwise_and(image, image, mask=mask == label)
        st.image(object, use_column_width=True)






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
        
        select_object(mask, image)

main()
