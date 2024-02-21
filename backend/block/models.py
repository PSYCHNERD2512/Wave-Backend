from django.db import models
from profiles.models import Profile

class Block(models.Model):
    sender = models.ForeignKey(Profile, related_name='blocked_profiles', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name='blocked_by_profiles', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender} blocked {self.receiver}"