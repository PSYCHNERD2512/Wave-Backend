from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

@api_view(['POST'])
def register(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     user = authenticate(username=username, password=password)

#     if user is None:
#         return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

#     refresh = RefreshToken.for_user(user)

#     return Response({
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }, status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    print("Received username:", username)
    print("Received password:", password)

    user = authenticate(username=username, password=password)

    if user is None:
        print("Authentication failed for user:", username)
        return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    print("Authentication successful for user:", username)

    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_200_OK)