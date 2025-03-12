from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from .models import Deal, Developer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied

from .serializers import DealSerializer, DeveloperSerializer, UserSerializer

class Home(APIView):
    def get(self, request):
        content = {"message": "Welcome to the brokeREd api home route"}
        return Response(content)

class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  
    refresh = RefreshToken.for_user(request.user) 
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })


class DealList(generics.ListCreateAPIView):
    serializer_class = DealSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
       user = self.request.user
       return Deal.objects.filter(user=user)
    
    def perform_create(self, serializer):
       serializer.save(user=self.request.user)


class DealDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DealSerializer
    lookup_field = "id"
    
    def get_queryset(self):
       user = self.request.user
       return Deal.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        developers_not_associated = Developer.objects.exclude(
            id__in=instance.developers.all()
        )
        developers_serializer = DeveloperSerializer(
            developers_not_associated, many=True
        )

        return Response(
            {
                "deal": serializer.data,
                "developers_not_associated": developers_serializer.data,
            }
        )
    def perform_update(self, serializer):
       deal = self.get_object()
       if deal.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to edit this deal."})
       serializer.save()
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
           raise PermissionDenied({"message": "You do not have permission to delete this deal."})
        instance.delete()

class DeveloperList(generics.ListCreateAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer


class DeveloperDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    lookup_field = "id"


class AddDeveloperToDeal(APIView):
    def post(self, request, deal_id, developer_id):
        deal = Deal.objects.get(id=deal_id)
        developer = Developer.objects.get(id=developer_id)
        deal.developers.add(developer)
        return Response({"message": f"{developer.name} added to Deal"})


class RemoveDeveloperFromDeal(APIView):
    def post(self, request, deal_id, developer_id):
        deal = Deal.objects.get(id=deal_id)
        developer = Developer.objects.get(id=developer_id)
        deal.developers.remove(developer)
        return Response({"message": f"{developer.name} removed from Deal {deal.name}"})
