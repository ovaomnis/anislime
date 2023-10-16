from rest_framework.permissions import BasePermission


class IsAuthorOrIsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        return request.user == obj.author or request.user.is_staff
