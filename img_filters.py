import streamlit as st
import cv2
import numpy as np

st.markdown("# Image Filter App")
st.markdown("Please upload an image using the button below and choose one of the filters from the dropdown menu to apply to the image. Use the sliders to adjust the filter parameters as needed.")

uploaded_file = st.file_uploader("Choose an image file", type="jpg")

if uploaded_file is not None:
    # Load the image using OpenCV
    image = cv2.imread(uploaded_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    st.image(image, caption="Original image", use_column_width=True)
    
    filters = ["Sharpen", "Canny edge detection", "Median filter", "Blur", "Contour"]
    filter_choice = st.selectbox("Choose a filter", filters)
    
    # Sharpen filter has no adjustable parameters
    if filter_choice == "Sharpen":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        filtered_image = cv2.filter2D(image, -1, kernel)
    
    # Canny edge detection filter has two adjustable parameters: sigma and lower/upper threshold
    elif filter_choice == "Canny edge detection":
        sigma = st.slider("Sigma", 0.0, 3.0, 0.5, 0.1)
        lower_threshold = st.slider("Lower threshold", 0, 255, 50)
        upper_threshold = st.slider("Upper threshold", 0, 255, 150)
        filtered_image = cv2.Canny(image, lower_threshold, upper_threshold, sigma)
    
    # Median filter has one adjustable parameter: size
    elif filter_choice == "Median filter":
        size = st.slider("Size", 3, 15, 3)
        filtered_image = cv2.medianBlur(image, size)
    
    # Blur filter has one adjustable parameter: kernel size
    elif filter_choice == "Blur":
        kernel_size = st.slider("Kernel size", 3, 15, 3)
        filtered_image = cv2.blur

    
    # Display the filtered image only after the user has chosen the values from the sliders
    if st.button("Apply"):
        st.image(filtered_image, caption=filter_choice, use_column_width=True)
