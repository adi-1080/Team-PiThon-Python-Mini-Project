from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class User(AbstractUser):
    is_pharmacy = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

class Pharmacy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    store_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.store_name

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturer = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Inventory(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='inventory')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('pharmacy', 'medicine')
    
    def __str__(self):
        return f"{self.pharmacy.store_name} - {self.medicine.name}"

@receiver(post_save, sender=Pharmacy)
def create_pharmacy_inventory(sender, instance, created, **kwargs):
    if created:
        Inventory.objects.bulk_create([
            Inventory(pharmacy=instance, medicine=medicine, quantity=0)
            for medicine in Medicine.objects.all()
        ])

class SMSRequest(models.Model):
    phone_number = models.CharField(max_length=15)
    medicine_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    response_sent = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.phone_number} - {self.medicine_name}"
