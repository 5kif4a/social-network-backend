# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Профиль пользователя
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True,
                               default="avatars/default_avatar.png")

    theme = models.ImageField(upload_to="themes/", null=True, blank=True,
                              default="themes/default_theme.jpg")

    status = models.CharField(max_length=140, null=True, blank=True, default="")

    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"Profile - User: {self.user.username} - E-Mail: {self.user.email}"


class Post(models.Model):
    """
    Пост
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    content = models.TextField()

    attachment = models.ImageField(upload_to="attachments/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post: {self.id} - User: {self.user.username} - {self.created_at}"

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
#
# class Comment(models.Model):
#     post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
#     author = models.CharField(max_length=200)
#     text = models.TextField()
#     created_date = models.DateTimeField(default=timezone.now)
#     approved_comment = models.BooleanField(default=False)
#
#     def approve(self):
#         self.approved_comment = True
#         self.save()
#
#     def __str__(self):
#         return self.text
#
#
# class Friend(models.Model):
#     pass
