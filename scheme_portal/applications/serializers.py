from rest_framework import serializers
from .models import  Application, Document
from users.models import UserProfile
from users.serializers import UserProfileSerializer
from scheme_manager.models import Scheme

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file']


class ApplicationSerializer(serializers.ModelSerializer):
    scheme_name = serializers.CharField(source='scheme.scheme_name', read_only=True)
    documents = serializers.ListField(
        child=serializers.FileField(),
        write_only=True
    )

    class Meta:
        model = Application
        fields = ['id', 'user', 'scheme', 'scheme_name', 'documents', 'status', 'date']
        extra_kwargs = {
            'user': {'read_only': True},
            'date': {'read_only': True},
            'status': {'read_only': True},
            'scheme': {'write_only': True}
        }

    def validate(self, attrs):
        scheme_id = attrs.get('scheme')
        if not scheme_id or not Scheme.objects.filter(id=scheme_id).exists():
            raise serializers.ValidationError('Invalid scheme ID')
        if Application.objects.filter(user=self.context['request'].user, scheme_id=scheme_id).exists():
            raise serializers.ValidationError('You have already applied for this scheme')
        return attrs
        

class ApplicationDetailSerializer(serializers.ModelSerializer):
    scheme_name = serializers.CharField(source='scheme.scheme_name', read_only=True)
    documents = DocumentSerializer(many=True,read_only=True)
    user_details=serializers.SerializerMethodField()
    date=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    eligibility_criteria=serializers.CharField(source='scheme.eligibility_criteria', read_only=True)
    class Meta:
        model = Application
        fields = ['id','scheme_name','eligibility_criteria','user_details','documents', 'status', 'date']
        extra_kwargs = {
            'date': {'read_only': True},
            'eligibility_criteria':{'read_only':True},
        }
    def get_user_details(self,obj):
        user=UserProfile.objects.filter(user=obj.user).first()
        return UserProfileSerializer(user).data

