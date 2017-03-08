import datetime
from django.db import models

# Create your models here.


class Feed(models.Model):
    link = models.CharField(max_length=200, primary_key=True)
    title = models.CharField(max_length=200, blank=False)
    pub_date = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-pub_date"]
