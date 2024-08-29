from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    karma = models.IntegerField()
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='chat_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='chat_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    following = models.ManyToManyField("self", symmetrical=False, related_name="followers", blank=True)


class Chat(models.Model):
    users = models.ManyToManyField(User)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)


class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)