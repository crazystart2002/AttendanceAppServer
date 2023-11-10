from django.db import models
from drf_extra_fields.fields import Base64ImageField
import base64
from io import BytesIO
from PIL import Image


#
# class registration_image(models.Model):
#     student_id = models.CharField(max_length=255)
#     image_name = models.CharField(max_length=255 )  # Field to store the image name
#     image = models.ImageField(upload_to='registration_images/')  # Use ImageField for image storage
#
#     def save(self, *args, **kwargs):
#         # Convert base64 image to PNG format before saving
#         if self.image.startswith('data:image/png;base64,'):
#             base64_data = self.image.split(',')[1]
#             image_data = BytesIO(base64.b64decode(base64_data))
#             self.image = None  # Clear the base64 image field
#             self.image_name = f"{self.student_id}.png"  # Set the image name
#             self.image.save(self.image_name, image_data, save=False)
#
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.image_name


class Face_Recognation(models.Model):
    student_Id = models.CharField(max_length=20)
    image = Base64ImageField()

class Face_Recognation2(models.Model):
    student_Id = models.CharField(max_length=20)
    image= models.ImageField(upload_to="Face_Recognation/media_image", default=None)