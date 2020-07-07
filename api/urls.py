from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet, UserPostsViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'user_posts', UserPostsViewSet, basename='user_posts')

urlpatterns = router.urls
