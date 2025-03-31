import streamlit as st
from datafetch import DataFetch
from classification import Classification

class Infected:
    def classification_app(self, classification, image, model_name):
        disease_name = classification.classification_process(model_name, image)
        
        return disease_name

    def crop_disease(self, datafetch, classification, uploaded_image):
        model_name = 'crop_type'
        
        crop_name = self.classification_app(classification, uploaded_image, model_name)
        
        crop_type_name = crop_name.lower()
        
        disease_name = self.classification_app(classification, uploaded_image, crop_type_name)
        
        disease_name = disease_name.replace('_', ' ').title()
        
        st.write(f"The crop disease is most likely **{disease_name}**")
        
        datafetch.infected_dataFetch(disease_name)

    def infected_crop_classify(self, uploaded_image):
        datafetch = DataFetch()
        classification = Classification()
        self.crop_disease(datafetch, classification, uploaded_image)