from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, PharmacyViewSet, MedicineViewSet, InventoryViewSet,
    UserRegistrationView, UserLoginView, MedicineSearchView, PharmacyInventoryView,
    Home
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'pharmacies', PharmacyViewSet)
router.register(r'medicines', MedicineViewSet)
router.register(r'inventory', InventoryViewSet)

urlpatterns = [
    path('', Home.as_view(), name='home'),  # Add this line for the home page
    path('api/', include(router.urls)),  # Move API routes under /api/
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('medicine/search/', MedicineSearchView.as_view(), name='medicine-search'),
    path('pharmacy/inventory/', PharmacyInventoryView.as_view(), name='pharmacy-inventory'),
]
