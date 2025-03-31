import cv2
import numpy as np
from PIL import Image
import tensorflow as tf

class Segmentation:
    def load_model(self):
        model = tf.keras.models.load_model('Models/unet_main.keras')
        
        return model
    
    # def replace_black_with_gray(self, image):
    #     if isinstance(image, Image.Image):  # Check if image is a PIL Image
    #         image = np.array(image)
        
    #     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #     lower_black = np.array([0, 0, 0], dtype=np.uint8)
    #     upper_black = np.array([50, 50, 50], dtype=np.uint8)  

    #     mask = cv2.inRange(image, lower_black, upper_black)

    #     gray_value=(128, 128, 128)
    #     image[mask == 255] = gray_value  

    #     final_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
    #     return final_image

    def calculate_disease_percentage(self, pred_mask):
        pred_mask = (pred_mask > 0.5).astype(np.uint8)
        contours, _ = cv2.findContours(pred_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        defected_area = sum([cv2.contourArea(cv2.convexHull(contour)) for contour in contours])
        total_area = pred_mask.shape[0] * pred_mask.shape[1]
        undefected_area = total_area - defected_area
        disease_percentage = (defected_area / total_area) * 100
        
        return defected_area, undefected_area, disease_percentage

    def preprocess_image(self, image):
        # if isinstance(image, np.ndarray):  # Convert NumPy array to PIL Image
        #     image = Image.fromarray(image)
            
        img = image.resize((256, 256))
        img_array = tf.keras.utils.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  
        
        return img_array

    def postprocess_mask(self, mask_array):
        mask_array = np.squeeze(mask_array)  
        mask_array = (mask_array > 0.5).astype(np.uint8) 
         
        return mask_array

    def segmentation_display(self, image, pred_mask):
        original_img = tf.keras.utils.img_to_array(image.resize((256, 256))) / 255.0 
        overlay = original_img.copy()
        overlay[pred_mask == 1, :] = [1, 0, 0]
        kernel_size = (1, 1)
        sigma = 10
        blurred_img = cv2.GaussianBlur(original_img, kernel_size, sigma)
        output_image = np.where(np.repeat(pred_mask[:, :, np.newaxis], 3, axis=2), overlay, blurred_img)
        
        final_image = (output_image * 255).astype(np.uint8) 
        
        return final_image

    def segmentation_process(self, image):
        model = self.load_model()
        
        # mod_image = self.replace_black_with_gray(image)
        image_array = self.preprocess_image(image)
        
        pred_mask = model.predict(image_array)
        
        pred_mask = self.postprocess_mask(pred_mask)
        output_image = self.segmentation_display(image, pred_mask)
        
        defected_area, undefected_area, disease_percentage = self.calculate_disease_percentage(pred_mask)
        
        return output_image, defected_area, undefected_area, disease_percentage