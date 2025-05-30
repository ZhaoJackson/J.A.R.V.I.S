import cv2
import numpy as np
from typing import Dict, Any
import base64
from io import BytesIO
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification

class VisionService:
    def __init__(self):
        # Initialize the model for activity recognition
        self.processor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")
        self.model = AutoModelForImageClassification.from_pretrained("microsoft/resnet-50")
        
    def process_image(self, image_data: str) -> Dict[str, Any]:
        """
        Process an image and return activity detection results
        """
        try:
            # Convert base64 image to numpy array
            image_bytes = base64.b64decode(image_data.split(',')[1])
            image = Image.open(BytesIO(image_bytes))
            
            # Process image for the model
            inputs = self.processor(images=image, return_tensors="pt")
            
            # Get predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = outputs.logits.softmax(dim=1)
                
            # Get top 3 predictions
            top3_prob, top3_indices = torch.topk(predictions, 3)
            
            results = {
                "activities": [
                    {
                        "activity": self.model.config.id2label[idx.item()],
                        "confidence": prob.item()
                    }
                    for prob, idx in zip(top3_prob[0], top3_indices[0])
                ]
            }
            
            return results
            
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")
            
    def get_activity_context(self, activities: list) -> str:
        """
        Generate a natural language description of the detected activities
        """
        context = "Based on the visual analysis, I can see that you are "
        
        if activities:
            main_activity = activities[0]
            context += f"primarily {main_activity['activity'].lower()} "
            context += f"(confidence: {main_activity['confidence']:.2%})"
            
            if len(activities) > 1:
                context += ". I also notice you might be "
                secondary_activities = [a['activity'].lower() for a in activities[1:]]
                context += " or ".join(secondary_activities)
        
        return context 