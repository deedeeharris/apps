import streamlit as st
from skimage import filters, color
import numpy as np

st.markdown("# Image Filter App")
st.markdown("Please upload an image using the button below and choose one of the filters from the dropdown menu to apply to the image. Use the sliders to adjust the filter parameters as needed.")

uploaded_file = st.file_uploader("Choose an image file", type="jpg")

if uploaded_file is not None:
    # Load the image using scikit-image
    image = color.rgb2gray(uploaded_file)
    
    st.image(image, caption="Original image", use_column_width=True)
    
    filters_list = ["Sharpen", "Canny edge detection", "Median filter", "Blur", "Contour"]
    filter_choice = st.selectbox("Choose a filter", filters_list)
    
    # Sharpen filter has no adjustable parameters
    if filter_choice == "Sharpen":
        filtered_image = filters.unsharp_mask(image, radius=1)
    
    # Canny edge detection filter has two adjustable parameters: sigma and lower/upper threshold
    elif filter_choice == "Canny edge detection":
        sigma = st.slider("Sigma", 0.0, 3.0, 0.5, 0.1)
        lower_threshold = st.slider("Lower threshold", 0, 1, 0.1)
        upper_threshold = st.slider("Upper threshold", 0, 1, 0.2)
        filtered_image = filters.canny(image, sigma=sigma, low_threshold=lower_threshold, high_threshold=upper_threshold)
    
    # Median filter has one adjustable parameter: size
    elif filter_choice == "Median filter":
        size = st.slider("Size", 3, 15, 3)
        filtered_image = filters.median(image, selem=np.ones((size, size)))
    
    # Blur filter has one adjustable parameter: kernel size
    elif filter_choice == "Blur":
        kernel_size = st.slider("Kernel size", 3, 15, 3)
        filtered_image = filters.gaussian(image, sigma=kernel_size)
    
    # Contour filter has one adjustable parameter: level
    elif filter_choice == "Contour":
        level = st.slider("Level", 0, 1, 0.5)
        filtered_image = filters.scharr(image) > level
    
    st.image(filtered_image, caption=f"Filtered image ({filter_choice})", use_column_width=True)
