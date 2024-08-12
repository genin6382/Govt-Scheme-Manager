from rest_framework.permissions import BasePermission

class ProfileOwner(BasePermission):
    
    def has_object_permission(self, request, view,obj):
        return obj.user==request.user 

class SchemeManager(BasePermission):
    def has_permission(self,request,view):
        return request.user.groups.filter(name='SchemeManager').exists()
    
    def has_object_permission(self,request,view,obj):
        return request.user.groups.filter(name='SchemeManager').exists()