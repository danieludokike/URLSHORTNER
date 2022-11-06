from django.db import models
from django.contrib.auth.models import User



class Urls(models.Model):
    """STORES THE LINKS SAVE BY THE USER"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.SlugField()
    shortened_url = models.SlugField()
    
    def __str__(self):
        return f"{self.url} -> {self.shortened_url}"