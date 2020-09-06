from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_dm import views

app_name = "dm"

# ModelsViewSetを継承して作成した場合のみ使用できる
router = DefaultRouter()
# 同じシリアライザーを参照している場合、basenameの指定が必要
router.register("message", views.MessageViewSet, basename="message")
router.register("inbox", views.InboxListView, basename="inbox")

urlpatterns = [path("", include(router.urls))]
