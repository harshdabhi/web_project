from django.contrib import admin
from .models import Collection, Machine, Warning, Fault, FaultEntry

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'importance')
    list_filter = ('status', 'collections')
    search_fields = ('name', 'description')
    filter_horizontal = ('collections', 'assigned_technicians', 'assigned_repair')

@admin.register(Warning)
class WarningAdmin(admin.ModelAdmin):
    list_display = ('machine', 'text', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('machine__name', 'text')
    raw_id_fields = ('machine', 'created_by')

@admin.register(Fault)
class FaultAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'machine', 'title', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('case_number', 'title', 'description', 'machine__name')
    raw_id_fields = ('machine', 'created_by')

@admin.register(FaultEntry)
class FaultEntryAdmin(admin.ModelAdmin):
    list_display = ('fault', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('fault__case_number', 'text', 'user__username')
    raw_id_fields = ('fault', 'user')
