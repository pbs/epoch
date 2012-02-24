from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save

""" A new model is needed for storing Rightscale credentials in the database """
class UserRightScaleProfile(models.Model):
    user = models.OneToOneField(User)
    
    rightscale_email = models.EmailField('rightscale e-mail address')
    rightscale_password = models.CharField('rightscale password', max_length=55)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserRightScaleProfile.objects.create(user=instance)
    
post_save.connect(create_user_profile, sender=User)