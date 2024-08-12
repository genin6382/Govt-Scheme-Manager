from rest_framework import generics
from rest_framework.response import Response
from .models import Application, Document
from .serializers import ApplicationSerializer,ApplicationDetailSerializer
from scheme_manager.permissions import IsSchemeManager
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.core.mail import send_mail
from scheme_manager.models import Scheme
from users.models import UserProfile


class ApplicationView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='SchemeManager').exists():
            return Application.objects.all()
        return Application.objects.filter(user=self.request.user)
      
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def post(self, request, *args, **kwargs):

        user = UserProfile.objects.filter(user=request.user).first()
        scheme_id = request.POST.get('scheme')
        scheme = Scheme.objects.filter(id=scheme_id).first()
        status = 'pending'
        validity=[]
        if (scheme.beneficiary_state != ['All']) and user.recidence_state not in scheme.beneficiary_state:
            status = 'rejected'
            validity.append('beneficiary_state')
        if  scheme.caste != ['All'] and user.caste not in scheme.caste:
            status = 'rejected'
            validity.append('caste')
        if user.age > scheme.age['general']['lte'] or user.age < scheme.age['general']['gte']:
            status = 'rejected'
            validity.append('age')
        if scheme.is_bpl==True and  user.is_bpl==False:
            status = 'rejected'
            validity.append('Below Poverty Line')
        if scheme.is_student != user.is_student:
            status = 'rejected'
            validity.append('Student')
        if scheme.disability==True and user.is_disabled==False:
            status = 'rejected'
            validity.append('Disability')
        if scheme.marital_status != ['All'] and user.marital_status not in scheme.marital_status:
            status = 'rejected'
            validity.append('marital_status')
           
        # Creating the application
        documents = request.FILES.getlist('documents')
        if not documents:
            return Response('Please upload documents', status=400)
        
        application = Application.objects.create(
            user=request.user,
            scheme=scheme,
            status=status
        )
        for document in documents:
            Document.objects.create(application=application, file=document)
        
        validity_message = ''
        if validity:
            validity_message = '\n\nValidity failed for: ' + ', '.join(validity)

        email_message = 'Your application has been submitted successfully.\n\nStatus: {}{}'.format(status, validity_message)

        send_mail(
            'Application Submitted',
            email_message,
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False
        )
        
        return Response('Application submitted successfully', status=201)
    
class ApplicationStatusView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        application = Application.objects.filter(scheme=self.kwargs['scheme_id'],user=self.request.user).first()
        if not application:
            return Response({'can_apply':True,'status':None}, status=200)
        
        return Response({'can_apply':False, 'status':application.status}, status=200)
    

class ApplicationDetailListView(generics.ListAPIView):
    serializer_class = ApplicationDetailSerializer
    permission_classes = [IsAuthenticated,IsSchemeManager]
    lookup_field = 'scheme_id'

    def get_queryset(self):
        try:
            return Application.objects.filter(scheme=self.kwargs['scheme_id']).order_by('date')
        except:
            return []

class ApplicationDetailManageView(generics.UpdateAPIView):
    serializer_class = ApplicationDetailSerializer
    permission_classes = [IsAuthenticated,IsSchemeManager]

    def put(self, request, *args, **kwargs):
        user = request.data.get('user')
        new_status = request.data.get('status')
        try:
            application = Application.objects.get(id=self.kwargs['pk'])
        except Application.DoesNotExist:
            return Response({"detail": "Application not found."}, status=404)
        except Application.MultipleObjectsReturned:
            return Response({"detail": "Multiple applications found."}, status=400)
        
        application.status = new_status
        application.save()
        message = (
            f"Dear {application.user.username},\n\n"
            "We wanted to inform you about the current status of your application for the scheme "
            f"'{application.scheme.scheme_name}'.\n\n"
            f"Status: {application.status.capitalize()}\n\n"
            "Please feel free to reach out if you have any questions or need further assistance.\n\n"
            "Best regards,\n"
            "The Application Support Team"
        )
        send_mail(
            'Update on your Application!',
            message,
            settings.EMAIL_HOST_USER,
            [application.user.email],
            fail_silently=False
        )
        serializer = self.serializer_class(application)
        return Response(serializer.data, status=200)