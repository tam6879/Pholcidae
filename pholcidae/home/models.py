from django.db import models

class CachedPage(models.Model):
    id = models.CharField(primary_key=True)
    text = models.CharField()
    image = models.CharField()
    time = models.DateTimeField()
    link1 = models.CharField()
    link2 = models.CharField()
    link3 = models.CharField()
    link4 = models.CharField()
