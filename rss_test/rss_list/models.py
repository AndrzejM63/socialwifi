from django.db import models

# Create your models here.


class Feed(models.Model):
    link = models.CharField(max_length=200, primary_key=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
