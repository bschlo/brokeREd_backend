from django.urls import path
from .views import Home, DealList, DealDetail, DeveloperList, DeveloperDetail, AddDeveloperToDeal, RemoveDeveloperFromDeal, CreateUserView, LoginView, VerifyUserView, TopBottomDealsView

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('deals/', DealList.as_view(), name='deal-list' ),
  path("deals/top-bottom/", TopBottomDealsView.as_view(), name="top-bottom-deals"),
  path('deals/<int:id>/', DealDetail.as_view(), name='deal-detail' ),
  path('developers/', DeveloperList.as_view(), name='developer-list'),
  path('developers/<int:id>/', DeveloperDetail.as_view(), name='developer-detail'),
  path('deals/<int:id>/add_developer/<int:developer_id>/', AddDeveloperToDeal.as_view(), name='add-developer-to-deal'),
  path('deals/<int:id>/remove_developer/<int:developer_id>/', RemoveDeveloperFromDeal.as_view(), name='remove-developer-from-deal'),
  path('users/register/', CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
]