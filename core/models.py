from django.db import models


class FBUser(models.Model):
    fbid = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)