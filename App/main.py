from PIL import Image
import streamlit as st
from healthy import Healthy
from infected import Infected
from segmentation import Segmentation
from classification import Classification

def classification_app(classification, image):
    st.write("Classifying...")
    
    model_name = 'infection'
    
    disease_name = classification.classification_process(model_name, image)
    
    return disease_name

def segmentation_app(segmentation, image):
    st.write("Segmenting...")
    
    input_image = Image.open(image)
    
    result_image, defected_pixels, undefected_pixels, disease_percentage = segmentation.segmentation_process(input_image)
    
    st.image(result_image, caption='Segmented Image.', use_column_width=True)
    
    # st.write(f"Defected Area (pixels): {defected_pixels}")
    # st.write(f"Undefected Area (pixels): {undefected_pixels}")
    st.write(f"Disease Percentage: {disease_percentage:.2f}%")
    
    return disease_percentage

def start_streamlit_app(classification, segmentation):
    st.title("🌿🍁 Crop Disease Classification and Segmentation 🌾🍀")
    st.header("Upload an image of the plant")
    
    uploaded_image = st.file_uploader("Choose an image...", type="jpg")

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        # st.image(image, caption='Uploaded Crop Image.', use_container_width =True)
        
        disease_percentage = segmentation_app(segmentation, uploaded_image)
        disease_name = classification_app(classification, uploaded_image)
        
        if(disease_name == 'Healthy'):
            st.write("The Crop is Healthy")
            healthy_classifier = Healthy() 
            healthy_classifier.healthy_crop_classify(uploaded_image)
        elif(disease_name == 'Infected'):
            st.write("The Crop is Infected")
            infected_classifier = Infected()
            infected_classifier.infected_crop_classify(uploaded_image)

if __name__ == "__main__":
    classification = Classification()
    segmentation = Segmentation()
    start_streamlit_app(classification, segmentation)