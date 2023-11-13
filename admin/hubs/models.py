from django.db import models

# Create your models here.
class Hubs(models.Model):
    hub = models.TextField()
    delay = models.PositiveIntegerField()