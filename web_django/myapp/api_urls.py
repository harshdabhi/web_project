from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    UserViewSet, CollectionViewSet, MachineViewSet, 
    WarningViewSet, FaultViewSet, FaultEntryViewSet
)
from .auth_views import CustomAuthToken, RegisterView, LogoutView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'collections', CollectionViewSet)
router.register(r'machines', MachineViewSet)
router.register(r'warnings', WarningViewSet)
router.register(r'faults', FaultViewSet)
router.register(r'fault-entries', FaultEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/token/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('auth/register/', RegisterView.as_view(), name='api_register'),
    path('auth/logout/', LogoutView.as_view(), name='api_logout'),
] 