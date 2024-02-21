from django.shortcuts import render
from django.http import JsonResponse
from .models import Profile
from .serializers import ProfileSerializer
from waving.models import Wave_Send
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@api_view(['GET', 'POST'])
def profile_list(request):
    if request.method == 'GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many = True)
        return Response({'profiles': serializer.data})
    
    if request.method == 'POST':
        serializer = ProfileSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET',  'DELETE'])
def profile_details(request, id):
    try:
        profile = Profile.objects.get(pk=id)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
@api_view(['PUT'])
def profile_update(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def disconnect_user(request,current_user_id, user_id):
    try:
        current_profile = Profile.objects.get(pk=current_user_id)
        user_to_disconnect = Profile.objects.get(pk=user_id)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        
        current_profile.connections.remove(user_to_disconnect)
        user_to_disconnect.connections.remove(current_profile)
        
        return Response({"message": "Disconnected from the user."}, status=status.HTTP_200_OK)