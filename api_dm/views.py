from rest_framework import authentication, permissions
from api_dm import serializers
from core.models import Message
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response


class MessageViewSet(viewsets.ModelViewSet):

    # Messageオブジェクトを全て取得
    queryset = Message.objects.all()
    # シリアライザーを指定
    serializer_class = serializers.MessageSerializer
    # 認証にトークンを使用
    authentication_classes = (authentication.TokenAuthentication,)
    # 認証済みのユーザーのみアクセス権限True
    permission_classes = (permissions.IsAuthenticated,)

    # 送信元のリストを取得
    def get_queryset(self):
        return self.queryset.filter(sender=self.request.user)

    # 作成 オーバーライド
    def perform_create(self, serializer):
        # saveする時senderにログインしているユーザーを自動的に割り当てる
        serializer.save(sender=self.request.user)

    # 削除 オーバーライド
    def destroy(self, request, *args, **kwargs):
        response = {"message": "Delete DM is not allowed"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # 更新 オーバーライド
    def update(self, request, *args, **kwargs):
        response = {"message": "Update DM is not allowed"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # 更新 オーバーライド
    def partial_update(self, request, *args, **kwargs):
        response = {"message": "Patch DM is not allowed"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class InboxListView(viewsets.ReadOnlyModelViewSet):

    # Messageオブジェクトを全て取得
    queryset = Message.objects.all()
    # シリアライザーを指定
    serializer_class = serializers.MessageSerializer
    # 認証にトークンを使用
    authentication_classes = (authentication.TokenAuthentication,)
    # 認証済みのユーザーのみアクセス権限True
    permission_classes = (permissions.IsAuthenticated,)

    # 自分宛のメッセージのみ取得(ログインしているユーザー指定)
    def get_queryset(self):
        return self.queryset.filter(receiver=self.request.user)