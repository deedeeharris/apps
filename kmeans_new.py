import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from skimage import io
from skimage.color import rgb2lab, deltaE_cie76

# Load image and convert to Lab color space
def load_image(image_path):
    image = io.imread(image_path)
    image = rgb2lab(image)
    return image

# Compute distance between two color vectors
def compute_distance(color_1, color_2):
    return deltaE_cie76(color_1, color_2)

# Compute k-means clustering
def compute_kmeans(image, k):
    # Extract color vectors
    image = image.reshape(image.shape[0] * image.shape[1], 3)
    
    # Initialize k-means model and fit to data
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(image)
    
    # Extract labels and cluster centers
    labels = kmeans.predict(image)
    centers = kmeans.cluster_centers_
    
    return labels, centers

# Create mask image
def create_mask(image, labels, centers):
    mask = np.zeros(image.shape[:2])
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            mask[i, j] = np.argmin([compute_distance(image[i, j, :], centers[k]) for k in range(centers.shape[0])])
    
    return mask

# App
def main():
    # Upload image
    image_path = st.file_uploader("Choose an image", type=["jpg", "png"])
    if not image_path:
        return
    image = load_image(image_path)
    
    # Select number of clusters
    k = st.sidebar.slider("Number of clusters", 2, 10, 5)
    
    # Compute k-means clustering
    labels, centers = compute_kmeans(image, k)
    
    # Create mask image
    mask = create_mask(image, labels, centers)
    
    # Display original image
    st.image(image_path, width=400)
    
    # Display mask image
    plt.imshow(mask, cmap="Accent")
    st.pyplot()
    
    # Download mask image
    if st.button("Download mask"):
        plt.imsave("mask.jpg", mask, cmap="Accent")
        st.markdown("<a href='mask.jpg' download>Download mask</a>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
