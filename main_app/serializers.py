from rest_framework import serializers
from .models import Deal, Developer
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
    
    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
          password=validated_data['password'] 
      )
      
      return user

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ['id', 'name']  

class DealSerializer(serializers.ModelSerializer):
    developers = serializers.PrimaryKeyRelatedField(queryset=Developer.objects.all(), many=True)  
    user = serializers.SerializerMethodField()

    class Meta:
        model = Deal
        fields = '__all__'

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username
        }

    def to_representation(self, instance):
        
        representation = super().to_representation(instance)
        
        
        developers = instance.developers.all()
        developers_serializer = DeveloperSerializer(developers, many=True)
        representation['developers'] = developers_serializer.data  
        
        return representation

    def update(self, instance, validated_data):
        
        developers_data = validated_data.pop('developers', None)


        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        
        if developers_data:
            
            instance.developers.set(developers_data)

        instance.save()  
        return instance



