from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Collection, Machine, Warning, Fault, FaultEntry
from .serializers import (
    UserSerializer, CollectionSerializer, MachineSerializer, 
    MachineStatusSerializer, WarningSerializer, FaultSerializer, 
    FaultEntrySerializer
)

class IsManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='Manager').exists()

class IsTechnicianOrRepairOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name__in=['Technician', 'Repair', 'Manager']).exists()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all().order_by('-importance', 'name')
    serializer_class = MachineSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    
    def get_queryset(self):
        queryset = Machine.objects.all().order_by('-importance', 'name')
        
        collection_id = self.request.query_params.get('collection', None)
        if collection_id:
            queryset = queryset.filter(collections__id=collection_id)
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        user = self.request.user
        assigned = self.request.query_params.get('assigned', None)
        if assigned == 'me':
            queryset = queryset.filter(
                Q(assigned_technicians=user) | Q(assigned_repair=user)
            ).distinct()
        
        return queryset
    
    @swagger_auto_schema(
        operation_description="Return a simplified status view of all machines",
        responses={200: MachineStatusSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def status(self, request):
        machines = self.get_queryset()
        serializer = MachineStatusSerializer(machines, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Assign a technician to a machine",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID of the technician')
            }
        ),
        responses={
            200: openapi.Response(description="Technician assigned successfully"),
            400: "User is not a technician",
            404: "User not found"
        }
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsTechnicianOrRepairOrReadOnly])
    def assign_technician(self, request, pk=None):
        machine = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            if not user.groups.filter(name='Technician').exists():
                return Response(
                    {'error': 'User is not a technician'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            machine.assigned_technicians.add(user)
            return Response({'status': 'technician assigned'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @swagger_auto_schema(
        operation_description="Assign repair personnel to a machine",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID of the repair personnel')
            }
        ),
        responses={
            200: openapi.Response(description="Repair personnel assigned successfully"),
            400: "User is not repair personnel",
            404: "User not found"
        }
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsTechnicianOrRepairOrReadOnly])
    def assign_repair(self, request, pk=None):
        machine = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            if not user.groups.filter(name='Repair').exists():
                return Response(
                    {'error': 'User is not repair personnel'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            machine.assigned_repair.add(user)
            return Response({'status': 'repair personnel assigned'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class WarningViewSet(viewsets.ModelViewSet):
    queryset = Warning.objects.all().order_by('-created_at')
    serializer_class = WarningSerializer
    permission_classes = [permissions.IsAuthenticated, IsTechnicianOrRepairOrReadOnly]
    
    def get_queryset(self):
        queryset = Warning.objects.all().order_by('-created_at')
        machine_id = self.request.query_params.get('machine', None)
        if machine_id:
            queryset = queryset.filter(machine_id=machine_id)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @swagger_auto_schema(
        operation_description="API endpoint for external systems to create warnings",
        request_body=WarningSerializer,
        responses={
            201: WarningSerializer,
            400: "Invalid request data"
        }
    )
    @action(detail=False, methods=['post'])
    def external_warning(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=None)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FaultViewSet(viewsets.ModelViewSet):
    queryset = Fault.objects.all().order_by('-created_at')
    serializer_class = FaultSerializer
    permission_classes = [permissions.IsAuthenticated, IsTechnicianOrRepairOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'case_number']
    
    def get_queryset(self):
        queryset = Fault.objects.all().order_by('-created_at')
        
        machine_id = self.request.query_params.get('machine', None)
        if machine_id:
            queryset = queryset.filter(machine_id=machine_id)
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        open_param = self.request.query_params.get('open', None)
        if open_param and open_param.lower() == 'true':
            queryset = queryset.exclude(status='RESOLVED')
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @swagger_auto_schema(
        operation_description="API endpoint for external systems to create faults",
        request_body=FaultSerializer,
        responses={
            201: FaultSerializer,
            400: "Invalid request data"
        }
    )
    @action(detail=False, methods=['post'])
    def external_fault(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=None)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Mark a fault as resolved",
        responses={
            200: FaultSerializer
        }
    )
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        fault = self.get_object()
        fault.status = 'RESOLVED'
        fault.save()
        serializer = self.get_serializer(fault)
        return Response(serializer.data)

class FaultEntryViewSet(viewsets.ModelViewSet):
    queryset = FaultEntry.objects.all().order_by('-created_at')
    serializer_class = FaultEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsTechnicianOrRepairOrReadOnly]
    
    def get_queryset(self):
        queryset = FaultEntry.objects.all().order_by('-created_at')
        
        fault_id = self.request.query_params.get('fault', None)
        if fault_id:
            queryset = queryset.filter(fault_id=fault_id)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 