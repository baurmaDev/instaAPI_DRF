from django.urls import path
from .views import (
    CreateUserAPIView,
    LoginAPIView,
    UserAccountAPIView,
    PostListCreateAPIView,
    PostRetrieveUpdateDeleteAPIView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', CreateUserAPIView.as_view(), name='user_registration'),
    path('user/login/', LoginAPIView.as_view(), name='user_login'),
    path('user/', UserAccountAPIView.as_view(), name='user_detail'),
    path('post/list-create/', PostListCreateAPIView.as_view(), name='post_list_create'),
    path('post/<int:pk>/', PostRetrieveUpdateDeleteAPIView.as_view(), name='post_retrieve_update_delete')
]
