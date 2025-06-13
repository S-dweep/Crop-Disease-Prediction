import numpy as np
from PIL import Image
import tensorflow as tf

class Classification:
    def __init__(self) -> None:
        # Mapping of model names to their respective class names
        self.model_class_mapping = {
            'apple_bell_pepper': ['Apple_Black_Rot', 'Apple_Cedar_Rust', 'Apple_Cedar_Rust', 'Apple_Scab', 'Bell_Pepper_Bacterial_Spot', 'Bell_Pepper_Leaf_Spot'],
            'corn': ['Corn_Common_Rust', 'Corn_Ear_Rot', 'Corn_Fall_Army_Worm', 'Corn_Grasshopper', 'Corn_Gray_Leaf_Spot', 'Corn_Leaf_Beetle', 'Corn_Leaf_Blight', 'Corn_Leaf_spot', 'Corn_Stem_Borer', 'Corn_Streak_Virus'],
            'cotton': ['Cotton_Bacterial_Blight', 'Cotton_Boll_Worm', 'Cotton_Mealy_Bug', 'Cotton_Red_Bug', 'Cotton_White_Fly'],
            'crop_type': ['Apple_Bell_Pepper', 'Corn', 'Cotton', 'Graph_Potato', 'Rice', 'Sugarcane', 'Tomato', 'Wheat', 'Z_Other'],
            'graph_potato': ['Grape_Esca_(Black_Measles)', 'Grape_Leaf_Blight', 'Graph_Black_Rot', 'Potato_Early_Blight', 'Potato_Late_Blight'],
            'healthy_crop': ['Apple_Healthy', 'Bell_Pepper_Healthy', 'Blueberry_Healthy', 'Cherry_Healthy', 'Corn_Healthy', 'Cotton_Healthy', 'Grape_Healthy', 'Peach_Healthy', 'Potato_Healthy', 'Raspberry_Healthy', 'Rice_Healthy', 'Soybean_Healthy', 'Strawberry_Healthy', 'Sugarcane_Healthy', 'Tomato_Healthy', 'Wheat_Healthy'],
            'infection': ['Healthy', 'Infected'],
            'rice': ['Rice_Bacterial_Blight', 'Rice_Brown_Spot', 'Rice_Hissa', 'Rice_Leaf_Blast', 'Rice_Neck_Blast', 'Rice_Tungro'],
            'sugarcane': ['Sugarcane_Bacterial_Blight', 'Sugarcane_Mosaic', 'Sugarcane_Red_Rot', 'Sugarcane_Red_Rust', 'Sugarcane_Yellow_Rust'],
            'tomato': ['Tomato_Bacterial_Spot', 'Tomato_Early_Blight', 'Tomato_Late_Blight', 'Tomato_Leaf_Blight', 'Tomato_Leaf_Curl', 'Tomato_Leaf_Mold', 'Tomato_Mosaic_Virus','Tomato_Septoria_Leaf_Spot', 'Tomato_Target_Spot', 'Tomato_Two_Spotted_Spider_Mites', 'Tomato_Verticillium _Wilt','Tomato_Yellow_Leaf_Curl'],
            'wheat': ['Wheat_Aphid', 'Wheat_Black_Rust', 'Wheat_Brown_Rust', 'Wheat_Flag_Smut', 'Wheat_Leaf_Blight', 'Wheat_Mite', 'Wheat_Powdery_Mildew', 'Wheat_Scab', 'Wheat_Stem_Fly', 'Wheat_Yellow_Rust'],
            'z_other': ['Cherry_Powdery_Mildew', 'Orange_Huanglongbing', 'Peach_Bacterial_Spot', 'Squash_Powdery_Mildew', 'Strawberry_Leaf_Scorch'],
        }

    def load_model(self, model_name) -> tf.keras.Model:
        model_path = f'Models/{model_name}.keras'   
        print(f"calling {model_name} model")
        # Load the pre-trained model
        if model_name not in self.model_class_mapping:
            raise ValueError(f"Model '{model_name}' not found in class name mapping.")
        model = tf.keras.models.load_model(model_path)
        print(f"Model '{model_name}' loaded successfully.")
        return model

    def load_image(self, image_path: str, target_size=(224,224)) -> tf.Tensor:
        img = Image.open(image_path)
        # Resize the image to the expected input size of the model
        img = img.resize(target_size) 
        # Convert the image to an array and normalize it
        img_array = tf.keras.utils.img_to_array(img)
        # expand dimensions to match the model's input shape
        img_array = tf.expand_dims(img_array, 0)  
        return img_array

    def predict_disease(self, image, model: tf.Tensor, model_name: str) -> str:
        """
        Predict the disease from the image using the specified model.
        Args:
            image (Image.Image): The input image to be classified.
            model (tf.keras.Model): The pre-trained model for classification.
            model_name (str): The name of the model being used.
        Returns:
            str: The predicted class name of the disease.
        """      
        # Ensure the model name is in lowercase to match the mapping
        if model_name is None or not isinstance(model_name, str) :
            raise ValueError("Model name cannot be None or empty.")
        model_name = model_name.lower()
        # Check if the model name exists in the mapping
        if model_name not in self.model_class_mapping:
            raise ValueError(f"Model '{model_name}' not found in class name mapping.")
        
        class_names = self.model_class_mapping[model_name]
        
        predictions = model.predict(image)
        
        score = tf.nn.softmax(predictions[0])
        
        max_index = np.argmax(score)
        max_class_name = class_names[max_index]
        max_score = score[max_index]
        
        print(f"Predicted class: {max_class_name} with probability {int(100 * max_score)}%")
        
        return max_class_name

    def classification_process(self, model_name: str, image: Image.Image) -> str:
        model = self.load_model(model_name)
        image = self.load_image(image)
        disease_name = self.predict_disease(image, model, model_name)
        return disease_name