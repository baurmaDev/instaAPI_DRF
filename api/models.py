from django.db import models
from django.dispatch import Signal
from django.contrib.auth.models import User

post_created = Signal()

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_account')
    nickname = models.CharField(max_length=30)
    bio = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=20)
    image_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Post(TimeStampedModel):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    caption = models.CharField(max_length=500)
    image_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.user.username}'s post"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        post_created.send(sender=self.__class__, post=self)
