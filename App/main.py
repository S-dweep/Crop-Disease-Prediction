from PIL import Image
import streamlit as st
from healthy_infected import Healthy, Infected
from segmentation import Segmentation
from classification import Classification

def classification_app(classification, image):
    model_name = 'infection'
    disease_name = classification.classification_process(model_name, image)
    return disease_name

def segmentation_app(segmentation, image):
    input_image = Image.open(image)
<<<<<<< HEAD
    result_image, disease_percentage, defection_ratio = segmentation.segmentation_process(input_image)
    return result_image, disease_percentage, defection_ratio
=======
    
    result_image, defected_pixels, undefected_pixels, disease_percentage = segmentation.segmentation_process(input_image)
    
    st.image(result_image, caption='Segmented Image.', use_container_width=True)
    
    # st.write(f"Defected Area (pixels): {defected_pixels}")
    # st.write(f"Undefected Area (pixels): {undefected_pixels}")
    st.write(f"Disease Percentage: {disease_percentage:.2f}%")
    
    return disease_percentage
>>>>>>> 3de164b3e6d86b53269a35b14396ff1e5401a308

def start_streamlit_app(classification, segmentation):
    st.title("🌿🍁 Crop Disease Classification and Segmentation 🌾🍀")
    st.header("Upload an image of a crop to classify and segment it for disease detection.")
    st.write("This application uses deep learning models to classify crop diseases and segment the affected areas in the image.")    
    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Original Image")
            st.image(image, caption='Uploaded Image.')
            st.write("### Uploaded Image Details")
            st.write(f"Image Size: {image.size[0]} x {image.size[1]}")
            st.write(f"Image Format: {image.format}")
            
        with col2:
            st.write("### Uploaded Image")
            result_image, disease_percentage, defection_ratio = segmentation_app(segmentation, uploaded_image)
            st.image(result_image, caption='Processed Image with Segmentation')
            st.write(f"Defection Ratio: {defection_ratio:.2f}")
            st.warning(f"### Disease Percentage: {disease_percentage:.2f}%")
            
        st.write("Classifying the crop disease...")
        st.write("### Classification Results:")    
        disease_name = classification_app(classification, uploaded_image)
                
        if(disease_name == 'Healthy'):
            st.success("The Crop is Healthy")
            healthy_classifier = Healthy() 
            class_name, data = healthy_classifier.healthy_crop_classify(uploaded_image)
            
            st.success(f"### The crop is most likely: {class_name}")
            
            st.write("\n### **Precautions You should take to keep your crop Healthy:**\n")
            for precaution in data["precautions"]:
                st.write(f"- {precaution}")
                
            st.write("\n### **Useful Fertilizers you can use in your crop:**\n")
            for fert in data["fertilizers"]:
                st.write(f"- {fert}")
            
            
        else:
            st.error("The Crop is Infected")
            infected_classifier = Infected()
            disease_name, data = infected_classifier.infected_crop_classify(uploaded_image)
            st.error(f"### The crop is most likely: {disease_name}")
            st.write("### **Prevention Remedies for this Crop Disease:**")
            for prevention_remedies in data["prevention_remedies"]:
                st.write(f"- {prevention_remedies}")


if __name__ == "__main__":
    classification = Classification()
    segmentation = Segmentation()
    start_streamlit_app(classification, segmentation)
