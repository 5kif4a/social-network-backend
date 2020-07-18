# Create your views here.
import json

from django.contrib.auth.models import User
from rest_framework import viewsets, status, generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Profile, Post, Friend
from .serializers import ProfileSerializer, UserPostSerializer, FriendSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id')
            user = User.objects.get(pk=user_id)
            user.first_name = request.data.get('first_name')
            user.last_name = request.data.get('last_name')
            user.save()

            new_profile = Profile(user=user)
            new_profile.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('pk')
            qs = Profile.objects.get(user_id=user_id)
            serializer = ProfileSerializer(qs)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            # parsing user data
            user_data = json.loads(request.data.get('user'))
            data['user'] = user_data

            instance = self.queryset.get(user_id=kwargs.get('pk'))

            instance.user.first_name = user_data.get('first_name', instance.user.first_name)
            instance.user.last_name = user_data.get('last_name', instance.user.last_name)
            instance.user.save()

            serializer = self.serializer_class(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserPostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = UserPostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def retrieve(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('pk')
            qs = self.queryset.filter(user_id=user_id).order_by('-created_at')
            if qs:
                serializer = self.serializer_class(qs, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# TODO User Searching by name
class ProfileSearchView(generics.ListAPIView):
    serializer_class = ProfileSerializer


class FriendsViewSet(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('pk')
            user_friends = self.queryset.filter(user_id=user_id)
            friends_profiles = [Profile.objects.get(user_id=friend.friend.id) for friend in user_friends]
            data = ProfileSerializer(friends_profiles, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
