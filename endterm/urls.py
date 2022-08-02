from django.urls import include, path
from . import views
# from . import api
from django.contrib.auth.decorators import login_required
urlpatterns = [

    path('register', views.register, name='register'),
    path('login', views.userlogin, name = 'login'),
    path('logout', views.userlogout, name = 'logout'),

    path('', views.index, name='index'),
    
    path('profile', views.userProfile, name = 'userProfile'),
    path('update', views.update, name = 'update'),
    path('profile&id=<int:user_id>/', views.viewuser, name='viewuser'),
    path('search', views.searchUser, name = 'search'),
    path('send', views.send,name = 'send'),
    path('checkRequest', views.checkRequest,name = 'checkRequest' ),
    path('friendlist', views.friendlist,name = 'friendlist' ),
    path('post', views.user_post, name = 'post'),

    path('roomchat_enter',views.roomchat_enter, name = 'roomchat_enter'),
    path('roomchat/<str:room_name>', views.roomchat, name='room'),

]