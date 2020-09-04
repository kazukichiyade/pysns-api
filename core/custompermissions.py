from rest_framework import permissions


# カスタムpermissions(プロフィールの更新・削除はログインしているユーザーのみ)
class ProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHOD = GET等
        if request.method in permissions.SAFE_METHODS:
            return True
        # DELETE等
        return obj.userPro.id == request.user.id