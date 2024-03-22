from rest_framework import serializers
from .models import Profile, Wave_Send
from django.contrib.auth import get_user_model

Profile = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    connections = serializers.PrimaryKeyRelatedField(many=True,queryset=Profile.objects.all())
    sent_waves = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    received_waves = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        
        
def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.personal_quotes = validated_data.get('personal_quotes', instance.personal_quotes)
        instance.interests = validated_data.get('interests', instance.interests)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.residence = validated_data.get('residence', instance.residence)
        instance.wave_buddy = validated_data.get('wave_buddy', instance.wave_buddy)
        instance.save()
        return instance


class WaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wave_Send
        fields = '__all__'
