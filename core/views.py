from django.shortcuts import render
from django.views import View
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User, Pharmacy, Pharmacist, Medicine, Inventory, SearchLog, SMSRequest
from .serializers import (
    UserSerializer, PharmacySerializer, PharmacistSerializer,
    MedicineSerializer, InventorySerializer, SearchLogSerializer,
    SMSRequestSerializer
)

class Home(View):
    def get(self, request):
        return render(request, 'core/home.html')

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="List all users",
        operation_description="Returns a list of all users in the system"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Create a new user",
        operation_description="Creates a new user with the provided information"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class PharmacyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing pharmacies.
    """
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer

    @swagger_auto_schema(
        operation_summary="List all pharmacies",
        operation_description="Returns a list of all pharmacies in the system"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class PharmacistViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing pharmacists.
    """
    queryset = Pharmacist.objects.all()
    serializer_class = PharmacistSerializer

class MedicineViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing medicines.
    """
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

    @swagger_auto_schema(
        operation_summary="List all medicines",
        operation_description="Returns a list of all medicines with their details"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class InventoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing inventory.
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    @swagger_auto_schema(
        operation_summary="Update inventory item",
        operation_description="Updates the inventory with new quantity information",
        request_body=InventorySerializer
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class SearchLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint for search analytics.
    """
    queryset = SearchLog.objects.all()
    serializer_class = SearchLogSerializer

class SMSRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing SMS requests.
    """
    queryset = SMSRequest.objects.all()
    serializer_class = SMSRequestSerializer

    @swagger_auto_schema(
        operation_summary="Create new SMS request",
        operation_description="Creates a new SMS request for medication inquiry",
        request_body=SMSRequestSerializer,
        responses={201: SMSRequestSerializer}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Here you would typically add SMS sending logic
        return Response(serializer.data, status=status.HTTP_201_CREATED)

