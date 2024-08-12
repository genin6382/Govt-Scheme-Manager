from rest_framework import generics
from .models import Scheme,Feedback
from .serializers import SchemeSerializer,FeedBackSerializer,FeedBackdetailSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSchemeManager,CanGiveFeedback,CanModifyFeedback
from rest_framework.permissions import SAFE_METHODS
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.response import Response

class SchemeList(generics.ListCreateAPIView):
    queryset = Scheme.objects.all().order_by('id')
    serializer_class = SchemeSerializer
    
    def get_permissions(self):

        if self.request.method in SAFE_METHODS:
            permission_classes=[IsAuthenticated]
        else:
            permission_classes=[IsAuthenticated,IsSchemeManager]
        
        return [permission() for permission in permission_classes]
    
    def post(self, request, *args, **kwargs):
        message = (
            f"Dear User,\n\n"
            "We are excited to announce the launch of a new scheme on our portal!\n\n"
            f"Scheme Name: {request.data['scheme_name']}\n\n"
            "Description: {request.data['summary']}\n\n"
            "This scheme offers a variety of benefits, including:\n"
            f"{request.data['benefits']}\n\n"
            "For more details on the scheme and to apply, please visit the following link:\n"
            f"{request.data['scheme_link']}\n\n"
            "We encourage you to take advantage of this opportunity. If you have any questions or need assistance, "
            "feel free to reach out to our support team.\n\n"
            "Best regards,\n"
            "The Scheme Portal Team"
        )
        send_mail(
            "New Scheme Launched on Scheme Portal",
            message,
            settings.EMAIL_HOST_USER,
            [person.email for person in User.objects.all()],
            fail_silently=False
        )
        return self.create(request, *args, **kwargs)

class SchemeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=SchemeSerializer
    
    def get_queryset(self):
        return Scheme.objects.filter(id=self.kwargs['pk'])
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            permission_classes=[IsAuthenticated]
        else:
            permission_classes=[IsAuthenticated,IsSchemeManager]
        return [permission() for permission in permission_classes]

    
    def delete(self, request, *args, **kwargs):
        scheme=Scheme.objects.filter(id=self.kwargs['pk']).first()
        message = (
            f"Dear User,\n\n"
            "We wanted to inform you that the scheme "
            f"'{scheme.scheme_name}' has expired and has been removed from the portal.\n\n"
            "If you have any questions or need further assistance, "
            "please feel free to reach out to our support team.\n\n"
            "Best regards,\n"
            "The Scheme Portal Team"
        )
        send_mail(
            "Scheme Removed from Scheme Portal",
            message,
            settings.EMAIL_HOST_USER,
            [person.email for person in User.objects.all()],
            fail_silently=False
        )
        return self.destroy(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        scheme=Scheme.objects.filter(id=self.kwargs['pk']).first()
        message = (
            f"Dear User,\n\n"
            "We wanted to inform you about the recent changes to the scheme "
            f"'{scheme.scheme_name}'.\n\n"
            "Please visit the following link to view the updated details:\n"
            f"{scheme.scheme_link}\n\n"
            "If you have any questions or need further assistance, "
            "please feel free to reach out to our support team.\n\n"
            "Best regards,\n"
            "The Scheme Portal Team"
        )
        send_mail(
            "Update on Scheme Details",
            message,
            settings.EMAIL_HOST_USER,
            [person.email for person in User.objects.all()],
            fail_silently=False
        )
        return self.update(request, *args, **kwargs)


class FeedbackView(generics.ListCreateAPIView):
    serializer_class=FeedBackSerializer

    def get_queryset(self):
        return Feedback.objects.filter(scheme=self.kwargs['pk']).select_related('user','scheme')
    
    def get_serializer_context(self):
        context= super().get_serializer_context()
        context['scheme_id']=self.kwargs['pk']
        return context
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            permission_classes=[IsAuthenticated]
        else:
            permission_classes=[IsAuthenticated,CanGiveFeedback]
        return [permission() for permission in permission_classes]
    
    def post(self, request, *args, **kwargs):
        scheme_id = self.kwargs['pk']
        user = self.request.user
        scheme = Scheme.objects.filter(id=scheme_id).first()

        if not scheme:
            raise Response({'scheme_id': 'Invalid scheme ID'}, status=400)

        Feedback.objects.create(
            user=user,
            scheme=scheme,
            rating=request.data['rating'],
            feedback=request.data['comment']
        )

        return Response({'message': 'Feedback submitted successfully'}, status=201)

class FeedbackDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=FeedBackdetailSerializer

    def get_queryset(self):
        return Feedback.objects.filter(id=self.kwargs['pk']).select_related('user','scheme')
    
    def get_permissions(self):
        permission_classes=[IsAuthenticated]

        if self.request.method not in SAFE_METHODS:
            permission_classes.append(CanModifyFeedback)

        return [permission() for permission in permission_classes]
    
    def get_serializer_context(self):
        context= super().get_serializer_context()
        context['scheme_id']=self.kwargs['scheme_id']
        return context
    
class CanGiveFeedbackView(generics.RetrieveAPIView):
    
    def get_permissions(self):
        permission_classes=[IsAuthenticated,CanGiveFeedback]
        return [permission() for permission in permission_classes] 
    def get(self,request,*args,**kwargs):
        feedback=Feedback.objects.filter(user=request.user,scheme=self.kwargs['pk']).first()
        if feedback:
            return Response({'can_feedback':False})
            
        else:
            return Response({'can_feedback':True})