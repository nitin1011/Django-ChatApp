# chat/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import JsonResponse, HttpResponse
from .models import Room, Message, Group, GroupMember
from datetime import datetime
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.core import serializers
from django.utils import timezone


@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.profile.is_online = True
    user.profile.save()


@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.profile.is_online = False
    user.profile.last_seen = timezone.now()
    user.profile.save()


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('user-list')
        else:
            return render(request, 'chat/login.html')
    else:
        return render(request, 'chat/login.html')


@login_required
def user_list(request):
    users = User.objects.all()
    user_list = []
    for i in users:
        if i.username != request.user.username:
            user_list.append(i)
    groups = GroupMember.objects.filter(member=request.user)
    return render(request, 'chat/user_list.html', {'users': user_list, 'groups': groups})


def room_create(request, pk):
    user = User.objects.get(pk=pk)
    username1 = user.username
    username2 = request.user.username
    if username1>username2:
        roomname = username1+username2
    else:
        roomname = username2+username1
    if Room.objects.filter(roomname = roomname).exists():
        room = Room.objects.get(roomname=roomname)
    else:
        room = Room.objects.create(roomname=roomname)
        room.save()
    return redirect('room', roomname)




def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    isgroup = False
    isadmin = False
    if Group.objects.filter(gname=room_name).exists():
        r_user = None
        group = Group.objects.get(gname=room_name)
        isgroup = True
        receiver_user = room_name
        if group.admin == request.user:
            isadmin = True
        if not GroupMember.objects.filter(group=group, member=request.user).exists():
            return redirect('login')
    elif not request.user.username in room_name:
        return redirect('login')
    else:
        receiver_user = room_name
        receiver_user = receiver_user.replace(request.user.username, '')
        r_user = User.objects.get(username=receiver_user)
    messages = Message.objects.filter(roomname=room_name)
    date = datetime.now()
    msg = {}
    for i in messages:
        if i.timestamp.date() == date.date() and 'today' not in msg.keys():
            msg['today'] = [i]
        elif i.timestamp.date() == date.date():
            msg['today'].append(i)
        elif i.timestamp.date() not in msg.keys():
            msg[str(i.timestamp.date())] = [i]
        else:
            msg[str(i.timestamp.date())].append(i)
    
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'receiver': r_user,
        'msg': msg,
        'isgroup': isgroup,
        'isadmin': isadmin,
    })


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2 and not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            user.save()
        return redirect('login')
    else:
        return render(request, 'chat/register.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='/chat/login/')
def create_group(request):
    if request.method == 'POST':
        group_name = request.POST['groupname']
        if Group.objects.filter(gname=group_name).exists():
            return redirect('user-list')
        group = Group.objects.create(gname = group_name, admin=request.user)
        group.save()
        group_member = GroupMember.objects.create(group=group, member=request.user)
        return redirect('room', group_name)
    else:
        return render(request, 'chat/create_group.html')


@login_required(login_url='/chat/login/')
def add_user_list(request, gname):
    users = User.objects.all()
    user_list = []
    for i in users:
        if i.username != request.user.username:
            user_list.append(i)
    return render(request, 'chat/user_list.html', {'user_list': user_list, 'groups': [], 'gname': gname})


@login_required(login_url='/chat/login/')
def group_member_list(request, gname):
    group_memeber = GroupMember.objects.all()
    members = []
    for member in group_memeber:
        if member.group.gname == gname:
            members.append(member.member)
    group = Group.objects.get(gname=gname)
    if group.admin == request.user:
        isadmin = True
    else:
        isadmin = False
    return render(request, 'chat/user_list.html', {'group_member': members, 'groups': [], 'gname':gname, 'isadmin': isadmin})


@login_required(login_url='/chat/login/')
def add_user(request, pk, gname):
    user = User.objects.get(pk=pk)
    group = Group.objects.get(gname=gname)
    if GroupMember.objects.filter(group=group, member=user).exists():
        return redirect('room', gname)
    groupmember = GroupMember.objects.create(group=group, member=user)
    groupmember.save()
    return redirect('room', gname)


def remove_user_group(request, pk, gname):
    user = User.objects.get(id=pk)
    group_member = GroupMember.objects.get(member=user)
    group_member.delete()
    return redirect('group-member-list', gname)


def img_message_save(request):
    print("dkhfioehf")
    if request.method == 'POST':
        img = request.FILES['img']
        user = request.POST['user']
        room_name = request.POST['room_name']
        print("image", img)
        print("user",user)
        print("Room name ",room_name)
        return JsonResponse({'success': 'image save'})