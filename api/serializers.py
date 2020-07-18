from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Profile, Post, Friend


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(partial=True)

    class Meta:
        model = Profile
        exclude = ('id', 'updated_at')

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.theme = validated_data.get('theme', instance.theme)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ('user', 'friend')
