from django.shortcuts import render
from django.http import JsonResponse
from .models import Profile
from block.models import Block
from .serializers import ProfileSerializer
from waving.models import Wave_Send
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    renderer_classes,
    permission_classes,
    authentication_classes,
)
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated


# Create your views here.
@api_view(["GET", "POST"])
@renderer_classes((JSONRenderer,))
@permission_classes((IsAuthenticated,))
def profile_list(request):
    if request.method == "GET":
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response({"profiles": serializer.data})

    if request.method == "POST":
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE"])
@renderer_classes((JSONRenderer,))
@permission_classes((IsAuthenticated,))
def profile_details(request, username):
    try:
        profile = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == "DELETE":
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["PATCH"])
@renderer_classes((JSONRenderer,))
@permission_classes((IsAuthenticated,))
def profile_update(request, username):
    try:
        profile = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PATCH":
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@renderer_classes((JSONRenderer,))
@permission_classes((IsAuthenticated,))
def disconnect_user(request, current_user_id, user_id):
    try:
        current_profile = Profile.objects.get(pk=current_user_id)
        user_to_disconnect = Profile.objects.get(pk=user_id)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if current_profile == user_to_disconnect:
        return Response(
            {"error": "You cannot disconnect from yourself."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not current_profile.connections.filter(pk=user_to_disconnect.pk).exists():
        return Response(
            {"error": "You are not connected with this user."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if request.method == "POST":

        current_profile.connections.remove(user_to_disconnect)
        user_to_disconnect.connections.remove(current_profile)

        return Response(
            {"message": "Disconnected from the user."}, status=status.HTTP_200_OK
        )


@api_view(["POST"])
@renderer_classes((JSONRenderer,))
@permission_classes((IsAuthenticated,))
def block_profile(request, sender_id, receiver_id):
    try:
        sender_profile = Profile.objects.get(pk=sender_id)
        receiver_profile = Profile.objects.get(pk=receiver_id)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if sender_profile == receiver_profile:
        return Response(
            {"error": "You cannot block yourself."}, status=status.HTTP_400_BAD_REQUEST
        )

    if sender_profile.connections.filter(pk=receiver_profile.pk).exists():
        sender_profile.connections.remove(receiver_profile)
        receiver_profile.connections.remove(sender_profile)

    if Block.objects.filter(sender=sender_profile, receiver=receiver_profile).exists():
        return Response(
            {"error": "You have already blocked this profile."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    block = Block(sender=sender_profile, receiver=receiver_profile)
    block.save()
    return Response(
        {"message": "Profile blocked successfully."}, status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
@renderer_classes((JSONRenderer,))
@permission_classes((IsAuthenticated,))
def unblock_profile(request, sender_id, receiver_id):
    try:
        sender_profile = Profile.objects.get(pk=sender_id)
        receiver_profile = Profile.objects.get(pk=receiver_id)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        if sender_profile == receiver_profile:
            return Response(
                {"error": "You cannot unblock yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        block = Block.objects.get(sender=sender_profile, receiver=receiver_profile)
        block.delete()
        return Response(
            {"message": "Profile unblocked successfully."}, status=status.HTTP_200_OK
        )
    except Block.DoesNotExist:
        return Response(
            {"error": "You have not blocked this profile."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
@permission_classes((IsAuthenticated,))
def profile_search(request):
    if request.method == "GET":
        filters = request.GET.get("filters")
        if not filters:
            return Response(
                {"error": "No filters provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        filtered_users = []
        filter_list = filters.lower().split(",")
        filter_list.sort()
        search_interests = filters.lower().split(",")
        search_interests.sort()
        for profile_data in serializer.data:
            for filter in filter_list:
                name = profile_data.get("name").lower().split(" ")
                if (
                    profile_data.get("name").lower() == filter.strip()
                    or filter.strip() in name
                ):
                    if profile_data not in filtered_users:
                        filtered_users.append(profile_data)
                        if filter in search_interests:
                            search_interests.remove(filter)

        filtered_users_name = []

        for user in filtered_users:
            interests = (user.get("interests")).lower()
            interests_list = interests.split(",")
            interests_list.sort()

            for interest in search_interests:
                if interest in interests_list:
                    break
                elif (
                    interest not in interests_list and interest == search_interests[-1]
                ):
                    filtered_users_name.append(user)
                    filtered_users.remove(user)

        filtered_users.extend(filtered_users_name)

        for profile_data in serializer.data:
            interests = (profile_data.get("interests")).lower()
            interests_list = interests.split(",")
            interests_list.sort()
            for interest in search_interests:
                if interest not in interests_list:
                    break
                elif interest in interests_list:
                    if profile_data not in filtered_users:
                        filtered_users.append(profile_data)

        return Response({"filtered_users": filtered_users})
