from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)           
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField()


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    roomname = models.CharField(max_length=100, default='')
    content = models.TextField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.author.username


class Room(models.Model):
    roomname = models.CharField(max_length=100)

    def __str__(self):
        return self.roomname


class Group(models.Model):
    gname = models.CharField(max_length=100)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.gname


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
