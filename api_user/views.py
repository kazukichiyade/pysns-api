from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from api_user import serializers
from core.models import Profile, FriendRequest
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from core import custompermissions


# ユーザーを新規作成するためのView(汎用ViewのCreateAPIViewを使用)
class CreateUserView(generics.CreateAPIView):
    # シリアライザーを指定するだけ
    serializer_class = serializers.UserSerializer


# 友達申請のViewSet
class FriendRequestViewSet(viewsets.ModelViewSet):
    # FriendRequestオブジェクトを全て取得
    queryset = FriendRequest.objects.all()
    # シリアライザーを指定
    serializer_class = serializers.FriendRequestSerializer
    # 認証にトークンを使用
    authentication_classes = (authentication.TokenAuthentication,)
    # 認証済みのユーザーのみアクセス権限True
    permission_classes = (permissions.IsAuthenticated,)

    # フィルタリング(一致したものだけを取得) オーバーライド
    def get_queryset(self):
        return self.queryset.filter(
            Q(askTo=self.request.user) | Q(askFrom=self.request.user)
        )

    # 作成 オーバーライド
    def perform_create(self, serializer):
        try:
            # saveする時askFromにログインしているユーザーを自動的に割り当てる
            serializer.save(askFrom=self.request.user)
        except:
            raise ValidationError("User can have only unique request")

    # 削除 オーバーライド
    def destroy(self, request, *args, **kwargs):
        response = {"message": "Delete is not allowed !"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # 更新 オーバーライド
    def partial_update(self, request, *args, **kwargs):
        response = {"message": "Patch is not allowed !"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# プロフィールViewSet
class ProfileViewSet(viewsets.ModelViewSet):
    # プロフィールのオブジェクトを全て取得
    queryset = Profile.objects.all()
    # シリアライザー指定
    serializer_class = serializers.ProfileSerializer
    # 認証にトークンを使用
    authentication_classes = (authentication.TokenAuthentication,)
    # 認証済みのユーザーのみアクセス権限True及びカスタムパーミッション指定(自身であれば削除、更新可能)
    permission_classes = (
        permissions.IsAuthenticated,
        custompermissions.ProfilePermission,
    )

    def perform_create(self, serializer):
        # saveする時userProにログインしているユーザーを自動的に割り当てる
        serializer.save(userPro=self.request.user)


class MyProfileListView(generics.ListAPIView):

    # プロフィールのオブジェクトを全て取得
    queryset = Profile.objects.all()
    # シリアライザー指定
    serializer_class = serializers.ProfileSerializer
    # 認証にトークンを使用
    authentication_classes = (authentication.TokenAuthentication,)
    # 認証済みのユーザーのみアクセス権限True及びカスタムパーミッション指定(自身であれば削除、更新可能)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # ログインしているユーザーに一致するプロフィールを取得
        return self.queryset.filter(userPro=self.request.user)