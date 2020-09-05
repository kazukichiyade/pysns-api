from django.urls import path, include
from api_user import views
from rest_framework.routers import DefaultRouter

app_name = "user"

# ModelsViewSetを継承して作成した場合のみしようできる
router = DefaultRouter()
router.register("profile", views.ProfileViewSet)
router.register("approval", views.FriendRequestViewSet)

# 汎用のAPIViewを作成した場合はこちらに記載する事(as_viewとnameが必要)
urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("myprofile/", views.MyProfileListView.as_view(), name="myprofile"),
    path("", include(router.urls)),
]