from django.db import models

class CachedPage(models.Model):
    # The 20 random characters in the URL
    id = models.CharField(primary_key=True)
    # The generated text content of the page
    text = models.CharField()
    # Image URL selected
    image = models.CharField()
    # The time the page was generated
    time = models.DateTimeField()
    # 4 links to go deeper into the tar pit
    link1 = models.CharField()
    link2 = models.CharField()
    link3 = models.CharField()
    link4 = models.CharField()
