from rest_framework.permissions import BasePermission
from applications.models import Application

class IsSchemeManager(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='SchemeManager').exists() or request.user.is_superuser
    
    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='SchemeManager').exists() or request.user.is_superuser

class CanGiveFeedback(BasePermission):

    def has_permission(self, request, view):
        scheme_id=view.kwargs['pk']
        return Application.objects.filter(user=request.user,scheme=scheme_id,status='approved').exists()
    
    def has_object_permission(self, request, view, obj):
        return obj.user==request.user
    
class CanModifyFeedback(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.user==request.user