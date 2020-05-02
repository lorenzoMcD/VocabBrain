from PIL import Image
from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Profile(models.Model):
    # creates one to many realtion ship
    # if user gets deleted cascade deletes profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'



    def save(self):
        super().save()

        img = Image.open(self.image.path)
        # resize larger images to smaller size
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
