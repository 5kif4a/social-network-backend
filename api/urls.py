from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet, UserPostsViewSet, FriendsViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'user_posts', UserPostsViewSet)
router.register(r'friends', FriendsViewSet)

urlpatterns = router.urls
