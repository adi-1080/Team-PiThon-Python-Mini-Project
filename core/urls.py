from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, PharmacyViewSet, PharmacistViewSet,
    MedicineViewSet, InventoryViewSet, SearchLogViewSet,
    SMSRequestViewSet, Home
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'pharmacies', PharmacyViewSet)
router.register(r'pharmacists', PharmacistViewSet)
router.register(r'medicines', MedicineViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'search-logs', SearchLogViewSet)
router.register(r'sms-requests', SMSRequestViewSet)

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('api/', include(router.urls)),
] 
