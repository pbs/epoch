from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save

""" A new model is needed for storing Rightscale credentials in the database """
class UserRightScaleProfile(models.Model):
    user = models.OneToOneField(User)
    
    rightscale_email = models.EmailField('rightscale e-mail address')
    rightscale_password = models.CharField('rightscale password', max_length=55)


class Deployment(models.Model):
    nickname = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    href = models.URLField(verify_exists=False)
    synced = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'%s' % self.nickname


class Server(models.Model):
    nickname = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    server_type = models.CharField(max_length=50)
    href = models.URLField(verify_exists=False)
    state = models.CharField(max_length=50)
    synced = models.BooleanField(default=False)
    deployment = models.ForeignKey(Deployment, blank=True, null=True)
    
    def __unicode__(self):
        return u'%s' % self.nickname
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserRightScaleProfile.objects.create(user=instance)
    
post_save.connect(create_user_profile, sender=User)