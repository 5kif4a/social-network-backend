# Create your models here.
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)


class Profile(models.Model):
    """
    Профиль пользователя
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True,
                               default="avatars/default_avatar.png")

    theme = models.ImageField(upload_to="themes/", null=True, blank=True,
                              default="themes/default_theme.jpg")

    status = models.CharField(max_length=140, null=True, blank=True, default="")

    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"Profile - User: {self.user.username} - E-Mail: {self.user.email}"


class Friend(models.Model):
    """
    Друг
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")

    def __str__(self):
        return f"Friendship: {self.user.username} - {self.friend.username}"


class Comment(models.Model):
    """
    Коммментарий
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username}"


class Post(models.Model):
    """
    Пост
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    content = models.TextField()

    attachment = models.ImageField(upload_to="attachments/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    comments = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Post by {self.user.username} - {self.created_at}"


class Chat(models.Model):
    """
    Чат
    """
    pass

# class Message(models.Model):
#     """
#     Сообщение
#     """
#     sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
#     receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
#     text = models.TextField()
#     sent_at = models.DateTimeField(auto_now=True)
#     delivered_at = models.DateTimeField()
#     read_at = models.DateTimeField()
