import streamlit as st
from PIL import Image, ImageFilter

st.markdown("# Image Filter App")
st.markdown("Please upload an image using the button below and choose one of the filters from the dropdown menu to apply to the image. Use the sliders to adjust the filter parameters as needed.")

uploaded_file = st.file_uploader("Choose an image file", type="jpg")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    st.image(image, caption="Original image", use_column_width=True)
    
    filters = ["Sharpen", "Canny edge detection", "Median filter", "Blur", "Contour"]
    filter_choice = st.selectbox("Choose a filter", filters)
    
    # Sharpen filter has no adjustable parameters
    if filter_choice == "Sharpen":
        filtered_image = image.filter(ImageFilter.SHARPEN)
    
    # Canny edge detection filter has two adjustable parameters: sigma and lower/upper threshold
    elif filter_choice == "Canny edge detection":
        sigma = st.slider("Sigma", 0.0, 3.0, 0.5, 0.1)
        lower_threshold = st.slider("Lower threshold", 0, 255, 50)
        upper_threshold = st.slider("Upper threshold", 0, 255, 150)
        filtered_image = image.filter(ImageFilter.Canny(sigma=float(sigma), lower=int(lower_threshold), upper=int(upper_threshold)))
    
    # Median filter has one adjustable parameter: size
    elif filter_choice == "Median filter":
        size = st.slider("Size", 3, 15, 3)
        filtered_image = image.filter(ImageFilter.MedianFilter(size=size))
    
    # Blur filter has one adjustable parameter: radius
    elif filter_choice == "Blur":
        radius = st.slider("Radius", 0, 10, 2)
        filtered_image = image.filter(ImageFilter.BLUR(radius=radius))
    
    # Contour filter has one adjustable parameter: scale
    elif filter_choice == "Contour":
        scale = st.slider("Scale", 0, 10, 1)
        filtered_image = image.filter(ImageFilter.CONTOUR(scale=scale))
    
    # Display the filtered image only after the user has chosen the values from the sliders
    if st.button("Apply"):
        st.image(filtered_image, caption=filter_choice, use_column_width=True)
