import streamlit as st
from datafetch import DataFetch
from classification import Classification

class Healthy:
    def healthy_crop_classify(self, image) -> dict:
        datafetch = DataFetch()
        classification = Classification()
        
        # It uses a model name 'healthy_crop' to classify the image.
        model_name = 'healthy_crop'
        # Call the classification process to get the class name
        class_name = classification.classification_process(model_name, image)
        # Format the class name to match the data fetch requirements from database
        formatted_class_name = class_name.split('_')[0]
        # Fetch healthy crop data from the database
        data = datafetch.healthy_dataFetch(formatted_class_name)
        
        return formatted_class_name, data
        
        
class Infected:
    def classification_app(self, classification, image, model_name) -> str:
        disease_name = classification.classification_process(model_name, image)
        return disease_name 

    def infected_crop_classify(self, uploaded_image):
        datafetch = DataFetch()
        classification = Classification()
        model_name = 'crop_type'
        crop_name = self.classification_app(classification, uploaded_image, model_name)
        crop_type_name = crop_name.lower()
        disease_name = self.classification_app(classification, uploaded_image, crop_type_name)
        formatted_disease_name = disease_name.replace('_', ' ').title()        
        data = datafetch.infected_dataFetch(formatted_disease_name)
        return formatted_disease_name, data