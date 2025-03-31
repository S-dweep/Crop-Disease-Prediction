import streamlit as st
from datafetch import DataFetch
from classification import Classification

class Healthy:
    def classification_app(self, classification, image):
        model_name = 'healthy_crop'
        
        disease_name = classification.classification_process(model_name, image)
        
        return disease_name

    def healthy_crop_type(self, datafetch, classification, uploaded_image):
        disease_name = self.classification_app(classification, uploaded_image)
        
        disease_name = disease_name.split('_')[0]
        
        st.write(f"The plant most likely belongs to **{disease_name}**")
        
        datafetch.healthy_dataFetch(disease_name)

    def healthy_crop_classify(self, uploaded_image):
        datafetch = DataFetch()
        classification = Classification()
        self.healthy_crop_type(datafetch, classification, uploaded_image)