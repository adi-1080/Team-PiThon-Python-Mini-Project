from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    preferred_language = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    is_smartphone_user = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Pharmacy(models.Model):
    pharmacy_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    location = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Pharmacies"

class Pharmacist(models.Model):
    pharmacist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} - {self.pharmacy.name}"

class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    alternative_medicines = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return f"{self.name} - {self.brand}"

class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.medicine.name} at {self.pharmacy.name}"

    class Meta:
        verbose_name_plural = "Inventories"

class SearchLog(models.Model):
    search_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    result_found = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} - {self.medicine_name}"

class SMSRequest(models.Model):
    sms_id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=15)
    medicine_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    response_sent = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.phone_number} - {self.medicine_name}"
