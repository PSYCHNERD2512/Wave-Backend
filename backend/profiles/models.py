from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length = 50)
    age = models.IntegerField()
    personal_quotes = models.CharField(max_length = 100)
    interests = models.CharField(max_length = 100)
    bio = models.CharField(max_length = 200)
    picture = models.CharField(max_length = 100)
    residence = models.CharField(max_length = 100)

    #link to the profile of best friend (optional)
    wave_buddy = models.CharField(max_length = 100)

    def __str__(self):
        return self.name + ' - ' + str(self.age)

