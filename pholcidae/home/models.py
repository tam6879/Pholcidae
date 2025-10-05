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

class BotProfile(models.Model):
    # The public IP of the bot
    ip_address = models.CharField(primary_key=True)
    # the date and time it first entered the tar pit
    enter_time = models.DateTimeField()
    # the number of pages it visited
    pages_visited = models.IntegerField(default=0)
    # The geographic location
    location = models.CharField()
    # A description of the device it's on
    device = models.CharField()
    # If it has been banned from the website
    is_banned = models.BooleanField(default=False)
