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
        fields = '__all__'
    
    def get_developer(self, obj):
        return {
            'id': obj.developer.id,
            'name': obj.developer.name
        }

class DealSerializer(serializers.ModelSerializer):
    developers = DeveloperSerializer(many=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Deal
        fields = '__all__'

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username
        }
    
    def create(self, validated_data):
        # Extract developers data from validated_data
        developers_data = validated_data.pop('developers', [])
        
        # Create the deal instance
        deal = Deal.objects.create(**validated_data)
        
        # Add the developers to the deal
        for developer_data in developers_data:
            # If you're using a many-to-many relationship
            # Assuming you have a Developer model with id and name fields
            developer_id = developer_data.get('id')
            if developer_id:
                # If you're using existing developers
                try:
                    developer = Developer.objects.get(id=developer_id)
                    deal.developers.add(developer)
                except Developer.DoesNotExist:
                    pass
            else:
                # If you're creating new developers
                name = developer_data.get('name')
                if name:
                    developer = Developer.objects.create(name=name)
                    deal.developers.add(developer)
        
        return deal

