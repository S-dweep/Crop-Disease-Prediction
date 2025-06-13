import cv2
import numpy as np
from PIL import Image
import tensorflow as tf

class Segmentation:
    def load_model(self) -> tf.keras.Model:
        # Load the pre-trained segmentation model
        model = tf.keras.models.load_model('Models/unet_main.keras') 
        print("Segmentation model loaded successfully.")
        return model

    def calculate_disease_percentage(self, pred_mask: np.ndarray) -> tuple:
        """Calculate the disease percentage and defection ratio from the predicted mask.
        This function computes the area of defects in the predicted mask and calculates
        the defection ratio and disease percentage based on the total area of the mask.
        The predicted mask is expected to be a binary mask where the defected areas are represented
        by values greater than 0.5.
        The defection ratio is calculated as the ratio of defected area to the undefected area.
        The disease percentage is calculated as the ratio of defected area to the total area of the mask,
        expressed as a percentage.
        

        Args:
            pred_mask (np.ndarray): The predicted mask from the segmentation model, expected to be a binary mask.

        Returns:
            tuple: A tuple containing the disease percentage and defection ratio.
            - disease_percentage (float): The percentage of the area that is defected.
            - defection_ratio (float): The ratio of defected area to undefected area.
        """
        pred_mask = (pred_mask > 0.5).astype(np.uint8)
        
        contours, _ = cv2.findContours(pred_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        defected_area = sum([cv2.contourArea(cv2.convexHull(contour)) for contour in contours])
        total_area = pred_mask.shape[0] * pred_mask.shape[1]
        
        undefected_area = total_area - defected_area
        defection_ratio = defected_area / undefected_area if total_area > 0 else 0
        disease_percentage = (defected_area / total_area) * 100
        return disease_percentage, defection_ratio

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess the input image for the segmentation model.
        This function resizes the input image to the expected input size of the model,
        converts it to an array, normalizes the pixel values, and expands the dimensions
        to match the model's input shape.
        Args:
            image (Image.Image): The input image to be preprocessed.
        Returns:
            np.ndarray: The preprocessed image as a numpy array, ready for model prediction.
        """         
        img = image.resize((256, 256))
        img_array = tf.keras.utils.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  
        return img_array

    def postprocess_mask(self, mask_array: np.ndarray) -> np.ndarray:
        """Postprocess the predicted mask from the segmentation model.
        This function squeezes the mask array to remove any singleton dimensions,
        thresholds the mask to create a binary mask, and converts it to an unsigned 8-bit integer format.
        Args:
            mask_array (np.ndarray): The predicted mask from the segmentation model.
        Returns:
            np.ndarray: The postprocessed binary mask as a numpy array.
        """
        mask_array = np.squeeze(mask_array)  
        mask_array = (mask_array > 0.5).astype(np.uint8) 
        return mask_array

    def segmentation_display(self, image: Image.Image, pred_mask: np.ndarray) -> np.ndarray:
        """Display the segmentation results by overlaying the predicted mask on the original image.
        This function creates an overlay of the predicted mask on the original image,
        blurs the original image, and combines the two to highlight the defected areas.
        Args:
            image (Image.Image): The original input image.
            pred_mask (np.ndarray): The predicted mask from the segmentation model.
        Returns:
            np.ndarray: The final output image with the segmentation overlay applied.
        """
        original_img = tf.keras.utils.img_to_array(image.resize((256, 256))) / 255.0 
        overlay = original_img.copy()
        overlay[pred_mask == 1, :] = [1, 0, 0]
        kernel_size = (1, 1)
        sigma = 10
        blurred_img = cv2.GaussianBlur(original_img, kernel_size, sigma)
        output_image = np.where(np.repeat(pred_mask[:, :, np.newaxis], 3, axis=2), overlay, blurred_img)
        final_image = (output_image * 255).astype(np.uint8) 
        return final_image

    def segmentation_process(self, image: Image.Image) -> tuple:
        """Process the input image for segmentation and return the output image with segmentation overlay.
        This function loads the segmentation model, preprocesses the input image,
        predicts the segmentation mask, postprocesses the mask, and displays the segmentation results.

        Args:
            image (Image.Image): The input image to be processed for segmentation.

        Returns:
            tuple: A tuple containing the output image with segmentation overlay,
                   the disease percentage, and the defection ratio.
        """
        model = self.load_model()
        image_array = self.preprocess_image(image)
        pred_mask = model.predict(image_array)
        pred_mask = self.postprocess_mask(pred_mask)
        output_image = self.segmentation_display(image, pred_mask)
        disease_percentage, defection_ratio = self.calculate_disease_percentage(pred_mask)
        return output_image, disease_percentage, defection_ratio