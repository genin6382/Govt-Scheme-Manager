from rest_framework import serializers
from .models import UserProfile
from django.db import transaction
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    username=serializers.CharField(allow_blank=False,allow_null=False,help_text='')
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True,style={'input_type':'password'})
    class Meta:
        model=User
        fields=['username','email','password']
    
    def validate(self, attrs):
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError('Username already exists')
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('Email already exists')
        return attrs
    
    @transaction.atomic
    def create(self,validated_data):
        password=validated_data.pop('password')
        user=User.objects.create_user(**validated_data)
        user.set_password(password)  
        user.save()
        if UserProfile.objects.filter(user=user).exists():
            serializers.ValidationError('Profile already exists')

        UserProfile.objects.create(user=user,age=1)
        return user  
          
class UserProfileSerializer(serializers.ModelSerializer):
    username=serializers.SerializerMethodField()
    email=serializers.SerializerMethodField()
    class Meta:
        model=UserProfile
        fields=['username','email','gender','recidence_state','recidence_district','caste','education','occupation','age','is_bpl','is_student','marital_status','is_disabled','phone_number']
        extra_kwargs={
            'age':{'min_value':1},
            'phone_number':{'min_length':10,'max_length':10},
        }
    
    def validate(self,attrs):
        phone_number=attrs.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise serializers.ValidationError('Phone number should contain only digits')
        
        profile=UserProfile.objects.filter(phone_number=phone_number).first()

        if profile and profile.user!=self.instance.user:
            raise serializers.ValidationError('Phone number already exists')
        return attrs
    def get_username(self,obj):
        return obj.user.username
    def get_email(self,obj):
        return obj.user.email

class GroupSerializer(serializers.ModelSerializer):
    username=serializers.CharField(help_text='')
    class Meta:
        model=User
        fields=['id','username']
    

    
        
    