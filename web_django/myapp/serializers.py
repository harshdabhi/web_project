from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Collection, Machine, Warning, Fault, FaultEntry

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name']

class WarningSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Warning
        fields = ['id', 'machine', 'text', 'created_by', 'created_at']
        read_only_fields = ['created_at']

class FaultEntrySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = FaultEntry
        fields = ['id', 'fault', 'text', 'user', 'image', 'created_at']
        read_only_fields = ['created_at']

class FaultSerializer(serializers.ModelSerializer):
    entries = FaultEntrySerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Fault
        fields = ['id', 'case_number', 'machine', 'title', 'description', 
                 'status', 'created_by', 'created_at', 'updated_at', 'entries']
        read_only_fields = ['case_number', 'created_at', 'updated_at']

class MachineSerializer(serializers.ModelSerializer):
    warnings = WarningSerializer(many=True, read_only=True)
    faults = FaultSerializer(many=True, read_only=True)
    collections = CollectionSerializer(many=True, read_only=True)
    assigned_technicians = UserSerializer(many=True, read_only=True)
    assigned_repair = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Machine
        fields = ['id', 'name', 'description', 'status', 'importance',
                 'collections', 'assigned_technicians', 'assigned_repair',
                 'created_at', 'updated_at', 'warnings', 'faults']
        read_only_fields = ['status', 'created_at', 'updated_at']

class MachineStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'name', 'status'] 