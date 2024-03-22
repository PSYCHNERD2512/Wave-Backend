from rest_framework import serializers
from .models import Profile, Wave_Send
from django.contrib.auth import get_user_model

Profile = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    connections = serializers.SerializerMethodField()
    sent_waves = serializers.SerializerMethodField()
    received_waves = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def get_connections_usernames(self, obj):
        return [connection.username for connection in obj.connections.all()]

    def get_sent_waves_usernames(self, obj):
        return [wave.from_profile.username for wave in obj.sent_waves.all()]

    def get_received_waves_usernames(self, obj):
        return [wave.to_profile.username for wave in obj.received_waves.all()]
        
        
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
