


import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from skimage import io
from skimage.color import rgb2lab, deltaE_cie76

st.set_option('deprecation.showPyplotGlobalUse', False)

def load_image(image_path):
    image = io.imread(image_path)
    image = rgb2lab(image)
    return image

def compute_distance(color_1, color_2):
    return deltaE_cie76(color_1, color_2)

def compute_kmeans(image, k):
    image = image.reshape(image.shape[0] * image.shape[1], 3)
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(image)
    labels = kmeans.predict(image)
    centers = kmeans.cluster_centers_
    return labels, centers

def create_mask(image, labels, centers):
    mask = np.zeros(image.shape[:2])
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            mask[i, j] = np.argmin([compute_distance(image[i, j, :], centers[k]) for k in range(centers.shape[0])])
    return mask

def main():
    image_path = st.file_uploader("Choose an image", type=["jpg", "png"])
    if not image_path:
        return
    image = load_image(image_path)
    k = st.sidebar.slider("Number of clusters", 2, 10, 5)
    labels, centers = compute_kmeans(image, k)
    mask = create_mask(image, labels, centers)
    st.image(image_path, width=400)
    plt.imshow(mask, cmap="Accent")
    st.pyplot()
    if st.button("Download mask"):
        with st.echo():
            buf = io.BytesIO()
            plt.imsave(buf, mask, cmap="Accent")
            buf.seek(0)
            st.markdown("<a href='#' download='mask.jpg'>Download mask</a>", unsafe_allow_html=True)
            st.write(buf.getvalue(), "image/jpeg", "mask.jpg")

if __name__ == "__main__":
    main()

