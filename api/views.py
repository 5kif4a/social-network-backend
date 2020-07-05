# Create your views here.
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Profile, Post
from .serializers import ProfileSerializer, UserPostSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        try:
            qs = Profile.objects.get(pk=user_id)
            serializer = ProfileSerializer(qs)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserPostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = UserPostSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        qs = Post.objects.filter(user_id=user_id).order_by('-created_at')
        if not qs:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserPostSerializer(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
