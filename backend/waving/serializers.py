from rest_framework import serializers
from .models import Wave_Send
class WaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wave_Send
        fields = '__all__'
