from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone_no = models.IntegerField(null=False)

    def __unicode__(self):
        return self.user.username