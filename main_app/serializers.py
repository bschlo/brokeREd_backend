from rest_framework import serializers
from .models import Deal, Developer
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
          email=validated_data['email'],
          password=validated_data['password'] 
      )
      
      return user

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = '__all__'

class DealSerializer(serializers.ModelSerializer):
    developers = DeveloperSerializer(many=True, read_only=True) 
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Deal
        fields = '__all__'

