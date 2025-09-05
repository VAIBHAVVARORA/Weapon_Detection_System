# models.py
from django.db import models
from django.shortcuts import render
from ultralytics import YOLO
from PIL import Image
import os
import sys

class CCTVImage(models.Model):
    image = models.ImageField(upload_to='cctv/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_image = models.ImageField(upload_to='cctv/processed_images/', blank=True, null=True)
    # Add any additional fields you need for your application

    def save(self, *args, **kwargs):
        # Override the save method to process the image before saving
        self.process_image()
        super().save(*args, **kwargs)

    def process_image(self):
        # Save the processed image
        model = YOLO('best.pt')
        img_count = 0
        image_paths = []
        image_directory = "E:\\Django\Weapon-Detection-Web-App\media\cctv\images" 
        for filename in os.listdir(image_directory):
            if filename.endswith(".jpg") or filename.endswith(".JPG") or filename.endswith(".jpeg") or filename.endswith(".png"):
                image_paths.append(os.path.join(image_directory, filename))
                img_count += 1

        print(f'Total number of images in the folder {image_directory} : ',img_count)

        count = 0
        for i in image_paths:
            results = model(i) 
            count += 1
            for r in results:
                im_array = r.plot() 
                im = Image.fromarray(im_array[..., ::-1])  
                im.save(f'E:\\Django\Weapon-Detection-Web-App\media\cctv\processed_images\{count}.jpg')  
                # processed_image_path = f'E:\\Django\Weapon-Detection-Web-App\media\cctv\processed_images\{count}.jpg'
                # self.processed_image = processed_image_path       
                # self.processed_image.save('processed_image.jpg', self.image, save=False)
            
            # Assign the processed image path to the processed_image field

        #self.processed_image = im.save(f'E:\\Django\Weapon-Detection-Web-App\media\cctv\processed_images\{count}.jpg')




