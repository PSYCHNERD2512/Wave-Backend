from django.shortcuts import render
from django.http import JsonResponse
from profiles.models import Profile
from .models import Wave_Send
from block.models import Block
from django.shortcuts import get_object_or_404
from .serializers import WaveRequestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def send_wave(request, sender_id, receiver_id):
    try:
        sender_profile = get_object_or_404(Profile, pk=sender_id)
        receiver_profile = get_object_or_404(Profile, pk=receiver_id)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if Block.objects.filter(sender=sender_profile, receiver=receiver_profile).exists():
        return Response({"error": "You cannot send a wave to a blocked profile."},
                        status=status.HTTP_400_BAD_REQUEST)

    if Block.objects.filter(sender=receiver_profile, receiver=sender_profile).exists():
        return Response({"error": "You cannot send a wave to a profile that has blocked you."},
                        status=status.HTTP_400_BAD_REQUEST)

    if sender_profile == receiver_profile:
        return Response({"error": "You cannot send a wave to yourself."},
                        status=status.HTTP_400_BAD_REQUEST)
        
    if sender_profile.connections.filter(pk=receiver_profile.pk).exists():
        return Response({"error": "You are already connected with this user."},
                        status=status.HTTP_400_BAD_REQUEST)
        
    if Wave_Send.objects.filter(from_profile=sender_profile, to_profile=receiver_profile, status='pending').exists():
        return Response({"error": "A wave is pending with the receiver."},
                        status=status.HTTP_400_BAD_REQUEST)

    wave_sent = Wave_Send(from_profile=sender_profile, to_profile=receiver_profile)
    wave_sent.save()
    
    sender_profile.sent_requests.add(receiver_profile)
    receiver_profile.received_requests.add(sender_profile)
    
    return Response({"message": "Wave sent successfully. Wave id is " + str(wave_sent.id)},
                    status=status.HTTP_201_CREATED)

@api_view(['POST'])
def accept_wave(request, request_id):
    try:
        wave_received = get_object_or_404(Wave_Send, pk=request_id)
    except Wave_Send.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if wave_received.status == 'accepted':
        return Response({"error": "Wave already accepted."},
                        status=status.HTTP_400_BAD_REQUEST)
    if wave_received.status == 'rejected':
        return Response({"error": "Wave already rejected."},
                        status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        wave_received.status = 'accepted'
        wave_received.save()
        
        sender_profile = wave_received.from_profile
        receiver_profile = wave_received.to_profile
        
        sender_profile.connections.add(receiver_profile)
        receiver_profile.connections.add(sender_profile)
        
        return Response({"message": "Wave accepted."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def reject_wave(request, request_id):
    try:
        wave_received = get_object_or_404(Wave_Send, pk=request_id)
    except Wave_Send.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if wave_received.status == 'accepted':
        return Response({"error": "Wave already accepted."},
                        status=status.HTTP_400_BAD_REQUEST)
    if wave_received.status == 'rejected':
        return Response({"error": "Wave already rejected."},
                        status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        wave_received.status = 'rejected'
        wave_received.save()
        
        
        return Response({"message": "Wave rejected."}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def list_waves(request):
    if request.method == 'GET':
        wavesHang = Wave_Send.objects.all()
        serializer = WaveRequestSerializer(wavesHang, many = True)
        return Response({'waves': serializer.data})
    