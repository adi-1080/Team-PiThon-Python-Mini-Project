from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from .models import User, Pharmacy, Medicine, Inventory
from .serializers import (
    UserSerializer, PharmacySerializer,
    MedicineSerializer, InventorySerializer, UserLoginSerializer
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
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                login(request, user)
                return Response({'message': 'Login successful'})
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PharmacyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing pharmacies.
    """
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer
    permission_classes = [AllowAny]  # Change this to IsAuthenticated after testing

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        pharmacy = serializer.save()
        # Inventory creation is handled by the post_save signal

class MedicineViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing medicines.
    """
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [AllowAny]  # Change this to IsAuthenticated after testing

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def search(self, request):
        name = request.query_params.get('name', '')
        medicines = Medicine.objects.filter(name__icontains=name)
        serializer = self.get_serializer(medicines, many=True)
        return Response(serializer.data)

class InventoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing inventory.
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_pharmacy:
            return Inventory.objects.filter(pharmacy__user=self.request.user)
        return Inventory.objects.none()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_medicine(self, request):
        pharmacy = request.user.pharmacy
        medicine_id = request.data.get('medicine_id')
        quantity = request.data.get('quantity', 0)

        try:
            inventory = Inventory.objects.get(
                pharmacy=pharmacy,
                medicine_id=medicine_id
            )
            inventory.quantity = quantity
            inventory.save()
        except Inventory.DoesNotExist:
            inventory = Inventory.objects.create(
                pharmacy=pharmacy,
                medicine_id=medicine_id,
                quantity=quantity
            )

        serializer = self.get_serializer(inventory)
        return Response(serializer.data)

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # If user is a pharmacy, create pharmacy profile
            if user.is_pharmacy:
                pharmacy_data = {
                    'store_name': request.data.get('store_name'),
                    'license_number': request.data.get('license_number'),
                    'user': user.id
                }
                pharmacy_serializer = PharmacySerializer(data=pharmacy_data)
                if pharmacy_serializer.is_valid():
                    pharmacy = pharmacy_serializer.save()
            
            return Response({
                'message': 'User registered successfully',
                'user_id': user.id,
                'is_pharmacy': user.is_pharmacy
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                return Response({
                    'message': 'Login successful',
                    'user_id': user.id,
                    'is_pharmacy': user.is_pharmacy
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MedicineListView(generics.ListAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]

class PharmacyInventoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_pharmacy:
            return Response({'error': 'Only pharmacies can access inventory'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        pharmacy = get_object_or_404(Pharmacy, user=request.user)
        inventory = Inventory.objects.filter(pharmacy=pharmacy)
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_pharmacy:
            return Response({'error': 'Only pharmacies can add to inventory'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        pharmacy = get_object_or_404(Pharmacy, user=request.user)
        serializer = InventorySerializer(data=request.data)
        
        if serializer.is_valid():
            # Check if medicine already exists in inventory
            existing_inventory = Inventory.objects.filter(
                pharmacy=pharmacy,
                medicine=serializer.validated_data['medicine']
            ).first()
            
            if existing_inventory:
                existing_inventory.quantity += serializer.validated_data['quantity']
                existing_inventory.save()
                return Response(InventorySerializer(existing_inventory).data)
            
            serializer.save(pharmacy=pharmacy)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MedicineSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        medicine_name = request.GET.get('name', '')
        # Always get all medicines and let JavaScript handle the filtering
        medicines = Medicine.objects.all()
        
        return render(request, 'core/medicine_search.html', {
            'medicines': medicines,
            'search_query': medicine_name
        })



