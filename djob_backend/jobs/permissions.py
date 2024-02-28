from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user and request.user.is_staff

class IsEmployerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        #  如果请求方法属于安全方法，允许访问
        if request.method in permissions.SAFE_METHODS:
           return True
        
        return request.user == obj.employer

class HandleAppicationIsEmployerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        #  如果请求方法属于安全方法，允许访问
        if request.method in permissions.SAFE_METHODS:
           return True
        
        return request.user == obj.created_for