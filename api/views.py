from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserAccount, Post
from .serializers import UserAccountSerializer, PostSerializer, LoginSerializer, UserSerializer

from .observers import NewPostNotification  # Import the observer class

import requests
#
# image_file = open('path/to/image.jpg', 'rb')
# response = requests.post('http://image-microservice/api/images/', files={'image': image_file})
# if response.status_code == 201:
#     image_url = response.json()['url']

class CreateUserAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # def perform_create(self, serializer):
    #     # Get the image from the request
    #     image = self.request.FILES.get('image')
    #
    #     # Make a request to the Image microservice to upload the image
    #     response = requests.post('http://127.0.0.1:8000/images/', files={'image': image})
    #
    #     # Get the image URL from the response
    #     image_url = response.json().get('image_url')
    #
    #     # Save the image URL to the user instance
    #     serializer.save(image_url=image_url)


class LoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)


class UserAccountAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAccountSerializer

    def get_object(self):
        print('-------------')
        print(self.request.user)
        print('-------------')
        return self.request.user.user_account


class PostListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user.user_account)

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user.user_account)  # Save the new post and get the object
        observers = [NewPostNotification()]  # Create a list of observers to notify
        for observer in observers:
            observer.update(sender=self, post=post)  # Notify each observer of the new post


class PostRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_object(self):
        return self.queryset.filter(user=self.request.user.user_account, id=self.kwargs['pk']).first()
