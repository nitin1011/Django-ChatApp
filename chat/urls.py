from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('img-message-save', views.img_message_save, name='img-save')
    path('user-list', views.user_list, name='user-list'),
    path('room-create/<int:pk>', views.room_create, name='room-create'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('create-group', views.create_group, name='create-group'),
    path('add-user-list/<str:gname>', views.add_user_list, name='add-user-list'),
    path('remove-user-group/<int:pk>/<str:gname>', views.remove_user_group, name='remove-user-group'),
    path('group-member-list/<str:gname>', views.group_member_list, name='group-member-list'),
    path('add-user/<int:pk>/<str:gname>', views.add_user, name='add-user'),
    path('<str:room_name>', views.room, name='room'),
]
