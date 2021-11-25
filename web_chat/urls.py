from django.urls import path
from .views import ChatRoom, RegisterUser, LogIn, LogOut, ChooseChatRoom
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'web_chat'
urlpatterns = [
    path('', LogIn.as_view(), name='login'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('chat/<str:room_name>/', ChatRoom.as_view(), name='chat'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('choosechat', ChooseChatRoom.as_view(), name='choosechat'),
]
