from django.db import models
from profiles.models import Profile
from django.utils import timezone


class Wave_Send(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ]
    from_profile = models.ForeignKey(Profile, related_name='sent_wave', on_delete=models.CASCADE)
    to_profile = models.ForeignKey(Profile, related_name='received_wave', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejected_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.from_profile} sent a wave to {self.to_profile} ({self.status})"