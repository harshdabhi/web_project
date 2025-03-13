from django.db import models
from django.contrib.auth.models import User

class Collection(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Machine(models.Model):
    STATUS_CHOICES = [
        ('OK', 'OK'),
        ('WARNING', 'Warning'),
        ('FAULT', 'Fault'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OK')
    importance = models.IntegerField(default=0)
    collections = models.ManyToManyField(Collection, related_name='machines', blank=True)
    assigned_technicians = models.ManyToManyField(User, related_name='assigned_machines_tech', blank=True, limit_choices_to={'groups__name': 'Technician'})
    assigned_repair = models.ManyToManyField(User, related_name='assigned_machines_repair', blank=True, limit_choices_to={'groups__name': 'Repair'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Warning(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='warnings')
    text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_warnings')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Warning on {self.machine.name}: {self.text[:50]}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.machine.status == 'OK':
            self.machine.status = 'WARNING'
            self.machine.save()

class Fault(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]
    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='faults')
    case_number = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_faults')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Fault #{self.case_number}: {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.case_number:
            last_fault = Fault.objects.order_by('-id').first()
            if last_fault:
                last_id = last_fault.id
            else:
                last_id = 0
            self.case_number = f"FAULT-{last_id + 1:06d}"
        
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new and self.machine.status != 'FAULT':
            self.machine.status = 'FAULT'
            self.machine.save()
        elif self.status == 'RESOLVED':
            open_faults = Fault.objects.filter(machine=self.machine).exclude(id=self.id).exclude(status='RESOLVED').exists()
            if not open_faults:
                has_warnings = Warning.objects.filter(machine=self.machine).exists()
                if has_warnings:
                    self.machine.status = 'WARNING'
                else:
                    self.machine.status = 'OK'
                self.machine.save()

class FaultEntry(models.Model):
    fault = models.ForeignKey(Fault, on_delete=models.CASCADE, related_name='entries')
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fault_entries')
    image = models.ImageField(upload_to='fault_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Entry on {self.fault.case_number} by {self.user.username}"
    
    class Meta:
        verbose_name_plural = "Fault Entries"
