from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserAccount, Post
from .serializers import UserAccountSerializer, PostSerializer, LoginSerializer, UserSerializer


class CreateUserAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer


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
    serializer_class = UserSerializer

    def get_object(self):
        print('-------------')
        print(self.request.user)
        print('-------------')
        return self.request.user


class PostListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user.user_account)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.user_account)


class PostRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_object(self):
        return self.queryset.filter(user=self.request.user.user_account, id=self.kwargs['pk']).first()
