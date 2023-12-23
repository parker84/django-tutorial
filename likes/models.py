from django.db import models
from django.contrib.auth.models import User # authenticate and authorize users
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class LikedItem(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE) # if a user is deleted, delete all the objects the user liked
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey()
