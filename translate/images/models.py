from django.db import models

# models.py
class Webtoon(models.Model):
    name = models.CharField(max_length=50)
    webtoon_img = models.ImageField(upload_to='images/')
