# models.py
from django.db import models
from django.shortcuts import render
from ultralytics import YOLO
from PIL import Image
import os
import sys

from django.conf import settings

# Global model loader to improve performance
# We use a lazy loading pattern or just load it once if possible
# But given the monkeypatch requirement, we need to apply it once globally or safely here

import torch
from ultralytics import YOLO

# Global variable to store the model
_YOLO_MODEL = None

def get_yolo_model():
    global _YOLO_MODEL
    if _YOLO_MODEL is None:
        # Monkeypatch torch.load to default weights_only=False
        original_load = torch.load
        try:
            torch.load = lambda *args, **kwargs: original_load(*args, **kwargs | {'weights_only': False})
            _YOLO_MODEL = YOLO('best.pt')
        finally:
            torch.load = original_load
    return _YOLO_MODEL

class CCTVImage(models.Model):
    image = models.FileField(upload_to='cctv/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_image = models.FileField(upload_to='cctv/processed_images/', blank=True, null=True)
    prediction = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.processed_image:
            try:
                self.process_image()
            except Exception as e:
                print(f"Error processing media: {e}")

    def process_image(self):
        try:
            model = get_yolo_model()
        except Exception as e:
            print(f"Model load error: {e}")
            return
        
        if not self.image:
            return

        media_path = self.image.path
        filename = os.path.basename(media_path)
        ext = os.path.splitext(filename)[1].lower()
        
        detected_classes = []
        
        # Only process images
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
        if ext in image_extensions:
            results = model(media_path)
            
            for r in results:
                for c in r.boxes.cls:
                    detected_classes.append(model.names[int(c)])
                
                im_array = r.plot()
                im = Image.fromarray(im_array[..., ::-1])
                
                processed_filename = f"processed_{filename}"
                processed_dir = os.path.join(settings.MEDIA_ROOT, 'cctv', 'processed_images')
                os.makedirs(processed_dir, exist_ok=True)
                
                processed_path = os.path.join(processed_dir, processed_filename)
                im.save(processed_path)
                
                self.processed_image.name = os.path.join('cctv', 'processed_images', processed_filename)
        else:
            print(f"Skipping non-image file: {filename}")
            
        # Update predictions
        if detected_classes:
            self.prediction = ", ".join(list(set(detected_classes)))
        else:
            self.prediction = "No detections"
            
        super().save(update_fields=['processed_image', 'prediction'])





