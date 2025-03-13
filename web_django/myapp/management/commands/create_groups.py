from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create default user groups'

    def handle(self, *args, **options):
        manager_group, created = Group.objects.get_or_create(name='Manager')
        technician_group, created = Group.objects.get_or_create(name='Technician')
        repair_group, created = Group.objects.get_or_create(name='Repair')
        view_only_group, created = Group.objects.get_or_create(name='View-only')
        
        self.stdout.write(self.style.SUCCESS('Successfully created user groups')) 