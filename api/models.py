from django.db import models
from django.contrib.auth.models import User

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30)
    bio = models.CharField(max_length=500)
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Post(TimeStampedModel):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='post_images/')
    caption = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.user.user.username}'s post"
