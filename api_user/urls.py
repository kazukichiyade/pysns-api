from django.urls import path, include
from rest_framework import DefaultRouter


app_name = "user"

router = DefaultRouter()

urlpatterns = [path("", include(router.urls))]
