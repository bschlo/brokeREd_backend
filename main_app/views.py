from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Deal, Developer
from .serializers import DealSerializer, DeveloperSerializer

class Home (APIView):
    def get(self, request):
        content = {'message': 'Welcome to the brokeREd api home route'}
        return Response(content)
    
class DealList(generics.ListCreateAPIView):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer

class DealDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    lookup_field = 'id'

class DeveloperList(generics.ListCreateAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer

class DeveloperDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    lookup_field = 'id'