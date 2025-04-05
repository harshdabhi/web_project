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
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser


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


@method_decorator(csrf_exempt, name='dispatch')
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        operation_description="Get all users in the Technician group",
        responses={200: UserSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def technicians(self, request):
        technicians = User.objects.filter(groups__name='Technician')
        serializer = self.get_serializer(technicians, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get all users in the Repair group",
        responses={200: UserSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def repair(self, request):
        repair_users = User.objects.filter(groups__name='Repair')
        serializer = self.get_serializer(repair_users, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    parser_classes = [JSONParser]


@method_decorator(csrf_exempt, name='dispatch')
class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all().order_by('-importance', 'name')
    serializer_class = MachineSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    parser_classes = [JSONParser]

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
        operation_description="Get all machines assigned to a specific user",
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_QUERY,
                description="ID of the user",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Filter by machine status",
                type=openapi.TYPE_STRING,
                required=False
            ),
        ],
        responses={200: MachineSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def assigned_to_user(self, request):
        user_id = request.query_params.get('user_id', None)
        status = request.query_params.get('status', None)

        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        if status == "All":
            status = None

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        machines = Machine.objects.filter(
            Q(assigned_technicians=user) | Q(assigned_repair=user)
        ).distinct()

        if status:
            machines = machines.filter(status=status)

        serializer = self.get_serializer(machines, many=True)
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
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsManagerOrReadOnly])
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
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsManagerOrReadOnly])
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


@method_decorator(csrf_exempt, name='dispatch')
class WarningViewSet(viewsets.ModelViewSet):
    queryset = Warning.objects.all().order_by('-created_at')
    serializer_class = WarningSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsTechnicianOrRepairOrReadOnly]
    parser_classes = [JSONParser]

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


@method_decorator(csrf_exempt, name='dispatch')
class FaultViewSet(viewsets.ModelViewSet):
    queryset = Fault.objects.all().order_by('-created_at')
    serializer_class = FaultSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsTechnicianOrRepairOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'case_number']
    parser_classes = [JSONParser, FormParser, MultiPartParser]

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


@method_decorator(csrf_exempt, name='dispatch')
class FaultEntryViewSet(viewsets.ModelViewSet):
    queryset = FaultEntry.objects.all().order_by('-created_at')
    serializer_class = FaultEntrySerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsTechnicianOrRepairOrReadOnly]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get_queryset(self):
        queryset = FaultEntry.objects.all().order_by('-created_at')

        fault_id = self.request.query_params.get('fault', None)
        if fault_id:
            queryset = queryset.filter(fault_id=fault_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
