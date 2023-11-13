from django.db import models

# Create your models here.
class Posts(models.Model):
    text = models.TextField()
    title = models.TextField()
    date = models.TextField()
    url = models.TextField()
    author = models.TextField()
    author_url = models.TextField()
    hub = models.TextField()
    post_id = models.PositiveIntegerField()