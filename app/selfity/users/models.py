import uuid
import random
from datetime import datetime
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from selfity.users.utils import make_thumbnail
from PIL import Image


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=10, null=False, blank=False,
                                    default="5555555555", unique=False,
                                    validators=[MinLengthValidator(10)])
    code = models.CharField(max_length=6, null=False, blank=False,
                            validators=[MinLengthValidator(10)],
                            default="246801")

    def save(self, *args, **kwargs):
        self.code = str(random.randint(100000, 999999))
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class Post(models.Model):
    image = models.ImageField(upload_to='photos/')
    mime_type = models.CharField(max_length=50)
    hashtag = models.CharField(unique=True, max_length=100)
    thumbnail = models.ImageField(upload_to='thumbnails/',editable=False, blank=True, null=True)
    latitude = models.CharField(max_length=40)
    longitude = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        make_thumbnail(self.thumbnail, self.image, (200, 200), 'thumb')
        super(Post, self).save(*args, **kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
