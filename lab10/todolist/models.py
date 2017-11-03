from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.username
