from rest_framework import serializers
from .models import Scheme,Feedback
from users.models import UserProfile

class SchemeSerializer(serializers.ModelSerializer):
    is_scheme_manager=serializers.SerializerMethodField()
    class Meta:
        model=Scheme
        fields='__all__'
    
    def get_is_scheme_manager(self,obj):
        request = self.context.get('request')
        if not request:
            return False
        return request.user.groups.filter(name='SchemeManager').exists()
    
class EligibleSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Scheme
        fields=['id','scheme_name']

class FeedBackSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source='user.username',read_only=True)
    gender=serializers.SerializerMethodField()
    
    class Meta:
        model=Feedback
        fields='__all__'
        extra_kwargs = {
            'date': {'read_only': True},
            'rating': {'required': True},
            'user':{'read_only':True},
            'scheme':{'read_only':True}
        }
    
    def validate(self, data):
        print("validated data:",data)
        user=self.context['request'].user
        scheme_id=self.context['scheme_id']
        feedback=Feedback.objects.filter(user=user,scheme_id=scheme_id).first()
        print(data)
        if feedback:
            raise serializers.ValidationError("Feedback already submitted")
        return data

    def get_gender(self,obj):
        profile=UserProfile.objects.filter(user=obj.user).first()
        return profile.gender

class FeedBackdetailSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source='user.username',read_only=True)
    is_user_feedback = serializers.SerializerMethodField()

    class Meta:
        model=Feedback
        fields='__all__'
        extra_kwargs = {
            'date': {'read_only': True},
            'rating': {'required': True},
            'user':{'read_only':True},
            'scheme':{'read_only':True}
        }
    def get_is_user_feedback(self,obj):
        request = self.context.get('request')
        if not request:
            return False
        user = request.user
        return obj.user == user
    