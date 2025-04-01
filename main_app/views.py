from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from .models import Deal, Developer, SavedDeal
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
        queryset = Deal.objects.filter(user=user)

        queryset = queryset.order_by('-date')
        
        stories_min = self.request.GET.get('storiesMin')
        print(stories_min)
        stories_max = self.request.GET.get('storiesMax')
        square_feet_min = self.request.GET.get('squareFeetMin')
        square_feet_max = self.request.GET.get('squareFeetMax')
        rate_type = self.request.GET.get('rateType')
        minimum_rate = self.request.GET.get('minimumRate')
        maximum_rate = self.request.GET.get('maximumRate')
        loan_amount_min = self.request.GET.get('loanAmountMin')
        loan_amount_max = self.request.GET.get('loanAmountMax')
        deal_type = self.request.GET.get('dealType')
        asset_class = self.request.GET.get('assetClass')
        developers = self.request.GET.get('developers')
        units_min = self.request.GET.get('unitsMin')
        units_max = self.request.GET.get('unitsMax')

        if stories_min:
            queryset = queryset.filter(stories__gte=stories_min)
        
        if stories_max:
            queryset = queryset.filter(stories__lte=stories_max)
        
        if square_feet_min:
            queryset = queryset.filter(square_feet__gte=square_feet_min)

        if square_feet_max:
            queryset = queryset.filter(square_feet__lte=square_feet_max)
        
        if rate_type:
            queryset = queryset.filter(rate_type=rate_type)
        
        if minimum_rate:
            queryset = queryset.filter(minimum_rate__gte=minimum_rate)
        if maximum_rate:
            queryset = queryset.filter(maximum_rate__lte=maximum_rate)
        
        if loan_amount_min:
            queryset = queryset.filter(loan_amount__gte=loan_amount_min)
        if loan_amount_max:
            queryset = queryset.filter(loan_amount__lte=loan_amount_max)
        
        if deal_type:
            queryset = queryset.filter(deal_type=deal_type)
        
        if asset_class:
            queryset = queryset.filter(asset_class=asset_class)
        
        if developers: 
           queryset = queryset.filter(developers=developers)

        if units_min: 
            queryset = queryset.filter(units__gte=units_min)
        
        if units_max: 
            queryset = queryset.filter(units__lte=units_max)

        sort_by_loan_amount = self.request.GET.get('sortByLoanAmount', 'asc')

        if sort_by_loan_amount == 'asc':
            queryset = queryset.order_by('loan_amount')
        elif sort_by_loan_amount == 'desc':
            queryset = queryset.order_by('-loan_amount')

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    
class TopBottomDealsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        
        top_5_loans = Deal.objects.filter(user=user).order_by("-loan_amount")[:5]
        bottom_5_loans = Deal.objects.filter(user=user).order_by("loan_amount")[:5]

        
        top_5_rates = Deal.objects.filter(user=user).order_by("-minimum_rate")[:5]
        bottom_5_rates = Deal.objects.filter(user=user).order_by("minimum_rate")[:5]

        return Response({
            "top_5_loans": DealSerializer(top_5_loans, many=True).data,
            "bottom_5_loans": DealSerializer(bottom_5_loans, many=True).data,
            "top_5_rates": DealSerializer(top_5_rates, many=True).data,
            "bottom_5_rates": DealSerializer(bottom_5_rates, many=True).data,
        })


class DealDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DealSerializer
    lookup_field = "id"
    
    def get_queryset(self):
        user = self.request.user
        return Deal.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Get developers not associated with this deal
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

      # Check if the user is allowed to edit this deal
      if deal.user != self.request.user:
          raise PermissionDenied({"message": "You do not have permission to edit this deal."})

      # Handle developers separately since it's a many-to-many relationship
      developers_data = self.request.data.get('developers', [])
      if developers_data:
          developers = Developer.objects.filter(id__in=developers_data)
          if len(developers) != len(developers_data):
              raise PermissionDenied({"message": "One or more developer IDs are invalid."})
          deal.developers.set(developers)

      latitude = self.request.data.get('latitude')
      longitude = self.request.data.get('longitude')

      if latitude and longitude:
          deal.latitude = latitude
          deal.longitude = longitude

      serializer.save()




class DeveloperList(APIView):
    def get(self, request, format=None):
        developers = Developer.objects.all().order_by('name')
        serializer = DeveloperSerializer(developers, many=True)
        return Response({'developers': serializer.data})


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

class SaveDealToProfile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, deal_id):

        user = request.user

        try:

            deal = Deal.objects.get(id=deal_id)

            existing_saved_deal = SavedDeal.objects.filter(user=user, deal=deal).first()

            if existing_saved_deal:
                
                existing_saved_deal.delete()
                return Response({"message": "Deal unsaved from profile"}, status=status.HTTP_200_OK)
            else:
                
                SavedDeal.objects.create(user=user, deal=deal)
                return Response({"message": "Deal saved to profile"}, status=status.HTTP_201_CREATED)
        
        except Deal.DoesNotExist:
            return Response({"error": "Deal not found"}, status=status.HTTP_404_NOT_FOUND)