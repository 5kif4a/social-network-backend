# Create your views here.
import json

from django.db.models import Q
from rest_framework import viewsets, status, filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Profile, Post, Friend, User
from .serializers import ProfileSerializer, UserPostSerializer, FriendSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    # profile searching
    search_fields = ['user__first_name', 'user__last_name']
    filter_backends = [filters.SearchFilter]

    # exclude from search result user himself & user friends
    def get_queryset(self):
        """
        SEARCH USERS
        """
        user_friends_ids = Friend.objects.filter(user=self.request.user).values_list('friend_id', flat=True)
        qs = self.queryset\
            .exclude(user=self.request.user)\
            .exclude(user_id__in=user_friends_ids)
        return qs

    def create(self, request, *args, **kwargs):
        """
        CREATE PROFILE
        """
        try:
            user_id = request.data.get('user_id')
            user = User.objects.get(pk=user_id)
            user.first_name = request.data.get('first_name')
            user.last_name = request.data.get('last_name')
            user.save()

            new_profile = Profile(user=user)
            new_profile.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        LIST OF PROFILES
        """
        try:
            user_id = kwargs.get('pk')
            qs = self.queryset.get(user_id=user_id)
            serializer = self.serializer_class(qs)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        UPDATE PROFILE DATA
        """
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
        """
        LIST OF USER POSTS
        """
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


class FriendsViewSet(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        USER'S FRIEND LIST
        """
        try:
            user_id = kwargs.get('pk')
            user_friends = self.queryset.filter(user_id=user_id)
            friends_profiles = [Profile.objects.get(user_id=friend.friend.id) for friend in user_friends]
            data = ProfileSerializer(friends_profiles, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        UNFRIEND USER
        """
        try:
            user_id = kwargs.get('pk')
            friend_id = request.data.get('friend_id')
            user_friend = self.queryset.filter(Q(user_id=user_id) & Q(friend_id=friend_id))
            user_friend.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
