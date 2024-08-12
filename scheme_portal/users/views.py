from rest_framework import generics,status
from .models import UserProfile
from django.contrib.auth.models import User,Group
from .serializers import UserProfileSerializer,UserSerializer,GroupSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import ProfileOwner,SchemeManager
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout


class Register(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes=[]

class Profile(generics.ListCreateAPIView):
    serializer_class=UserProfileSerializer
    permission_classes=[IsAuthenticated,ProfileOwner]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def get(self,request):
        user=self.request.user
        try:
            profile=UserProfile.objects.filter(user=user).first()
            serializer=self.serializer_class(profile)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error':'Profile not found'},status=status.HTTP_404_NOT_FOUND)

    def post(self,request):
        user=self.request.user
        try:
            print(request.data)
            profile=UserProfile.objects.filter(user=user).first()
            serializer=self.serializer_class(profile,data=self.request.data,partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            print(serializer.errors)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({'error':'Profile not found'},status=status.HTTP_404_NOT_FOUND)
        
    def delete(self,request):
        user=self.request.user
        try:
            user.delete()
            logout(request)
            return Response({'message':'Profile deleted'},status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error':'Profile not found'},status=status.HTTP_404_NOT_FOUND)

class ManageGroups(generics.ListCreateAPIView):
    serializer_class=GroupSerializer
    permission_classes=[IsAuthenticated,SchemeManager]
    
    def get_queryset(self):
         return User.objects.filter(groups__name='SchemeManager')

    def post(self,request):
        attrs=request.data.copy()
        username=attrs.get('username')
        user=User.objects.filter(username=username).first()
        if not user:
            return Response({'error':'User not found'},status=status.HTTP_404_NOT_FOUND)
        if user.groups.filter(name='SchemeManager').exists():
            return Response({'error':'User already in SchemeManager group'},status=status.HTTP_400_BAD_REQUEST)
        
        group=Group.objects.filter(name='SchemeManager').first()
        user.groups.add(group)
        user.save()
        return Response({'message':'User added to SchemeManager group'},status=status.HTTP_200_OK)
    
class RemoveManager(generics.RetrieveDestroyAPIView):
    serializer_class=GroupSerializer
    permission_classes=[IsAuthenticated,SchemeManager]

    def get_object(self):
        user=User.objects.filter(id=self.kwargs['pk']).first()
        if not user:
            return None
        if not user.groups.filter(name='SchemeManager').exists():
            return None
        return user
        
    def delete(self,request,*args,**kwargs):
        user=self.get_object()
        if user is None:
            return Response({'error':'User not found'},status=status.HTTP_404_NOT_FOUND)
        group=Group.objects.filter(name='SchemeManager').first()
        user.groups.remove(group)
        user.save()
        return Response({'message':'User removed from SchemeManager group'},status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@csrf_protect
def Login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return Response({'message': 'User already logged in'}, status=status.HTTP_200_OK)
        return Response({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'POST':
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(Response.status_code)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(generics.CreateAPIView):
    def post(self,request):
        logout(request)
        return Response({'message':'Logout successful'},status=status.HTTP_200_OK)