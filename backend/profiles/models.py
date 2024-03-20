from django.db import models
from django.contrib.auth.models import AbstractUser
import base64

def imgtostr(image):
    with open(image) as img:
        encoded_str = base64.b64encode(img.read())
        return encoded_str

class Profile(AbstractUser):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    about = models.CharField(max_length=150)
    interests = models.CharField(max_length=100)
    picture = models.CharField(max_length=100000)
    residence = models.CharField(max_length=100)
    wave_buddy = models.CharField(max_length=100)
    connections = models.ManyToManyField('self', symmetrical=True, blank=True)
    sent_requests = models.ManyToManyField('self', symmetrical=False, related_name='sent_wave_requests', through='Wave_Send', through_fields=('from_profile', 'to_profile'), blank=True)
    received_requests = models.ManyToManyField('self', symmetrical=False, related_name='received_wave_requests', through='Wave_Send', through_fields=('to_profile', 'from_profile'), blank=True)



    def __str__(self):
        return self.name + ' - ' + str(self.age)

class Wave_Send(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ]
    from_profile = models.ForeignKey(Profile, related_name='sent_waves', on_delete=models.CASCADE)
    to_profile = models.ForeignKey(Profile, related_name='received_waves', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.from_profile} sent a wave to {self.to_profile} ({self.status})"
