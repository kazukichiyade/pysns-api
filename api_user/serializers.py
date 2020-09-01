from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from core.models import Profile, FriendRequest


# Serializer = Django FormのAPI用
# 複雑な入力値をモデルに合わせてバリデーションしてレコードに伝えたり(入力)
# Model(レコード)を適切な形式にフォーマットしたり(出力)
# と言った具合に、 APIの リクエスト / レスポンス に特化した機能を提供します。


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    # createメソッドをオーバーライド(userを新規作成した場合、Token生成しDBへ)
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):

    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "nickName", "userPro", "created_on", "img")
        extra_kwargs = {"userPro": {"read_only": True}}


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ("id", "askFrom", "askTo", "approved")
        extra_kwargs = {"askFrom": {"read_only": True}}
