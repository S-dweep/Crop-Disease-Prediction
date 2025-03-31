import streamlit as st
from pymongo import MongoClient

class DataFetch:
    def healthy_dataFetch(self, healthy_crop_name):
        client = MongoClient("mongodb://localhost:27017/")  
        db = client["Crop_Disease_Prediction"]
        collection = db["Healthy_Crop"]

        doc = collection.find_one({"name": healthy_crop_name})
            
        if doc:
            print(f"\nCrop: {doc['name']}")
        
            st.write("\n**Precautions You should take to keep your crop Healthy:**\n")
            for precaution in doc["precautions"]:
                st.write(f"- {precaution}")
                
            st.write("\n**Useful Fertilizers you can use in your crop:**\n")
            for fert in doc["fertilizers"]:
                st.write(f"- {fert}")
        else:
            print(f"\nNo data found for '{healthy_crop_name}'.")
        
        client.close()
        
    def infected_dataFetch(self, infected_crop_name):
        client = MongoClient("mongodb://localhost:27017/")  
        db = client["Crop_Disease_Prediction"]
        collection = db["Infected_Crop"]

        doc = collection.find_one({"disease": infected_crop_name})
            
        if doc:
            print(f"\nCrop: {doc['disease']}")
            
            st.write("\n**Prevention Remedies for this Crop Disease:**\n")
            for prevention_remedies in doc["prevention_remedies"]:
                st.write(f"- {prevention_remedies}")
        else:
            print(f"\nNo data found for '{infected_crop_name}'.")
        
        client.close()


        
        