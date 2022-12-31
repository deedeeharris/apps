import streamlit as st
from PIL import Image, ImageFilter

# Display instructions to the user
st.markdown("# Image Filter App")
st.markdown("Please upload an image using the button below and choose one of the filters from the dropdown menu to apply to the image.")

# Allow the user to upload an image
uploaded_file = st.file_uploader("Choose an image file", type="jpg")

# Open the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Display the original image
    st.image(image, caption="Original image", use_column_width=True)
    
    # Create a list of filters
    filters = ["Sharpen", "Canny edge detection", "Median filter", "Blur", "Contour"]
    
    # Allow the user to choose a filter from the dropdown menu
    filter_choice = st.selectbox("Choose a filter", filters)
    
    # Apply the selected filter to the image
    if filter_choice == "Sharpen":
        filtered_image = image.filter(ImageFilter.SHARPEN)
    elif filter_choice == "Canny edge detection":
        filtered_image = image.filter(ImageFilter.FIND_EDGES)
    elif filter_choice == "Median filter":
        filtered_image = image.filter(ImageFilter.MedianFilter(size=3))
    elif filter_choice == "Blur":
        filtered_image = image.filter(ImageFilter.BLUR)
    elif filter_choice == "Contour":
        filtered_image = image.filter(ImageFilter.CONTOUR)
    
    # Display the filtered image
    st.image(filtered_image, caption=filter_choice, use_column_width=True)
