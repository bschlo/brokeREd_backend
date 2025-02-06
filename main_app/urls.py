from django.urls import path
from .views import Home, DealList, DealDetail, DeveloperList, DeveloperDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('deals/', DealList.as_view(), name='deal-list' ),
  path('deals/<int:id>/', DealDetail.as_view(), name='deal-detail' ),
  path('developers/', DeveloperList.as_view(), name='developer-list'),
  path('developers/<int:id>/', DeveloperDetail.as_view(), name='developer-detail'),
]