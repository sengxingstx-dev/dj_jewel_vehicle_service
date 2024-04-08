from django.db import models
from django.db.models import Sum

from .utils.files import (
    max_file_size_validator,
    validate_image_extension,
    agent_storage,
    customer_storage,
    car_storage,
    payment_storage,
)
from apps.account.models import Account


class Customer(models.Model):
    # customer_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        default='default_profiles/default.jpg',
        upload_to=customer_storage,
        null=True,
        blank=True,
        validators=[validate_image_extension, max_file_size_validator],
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user}'

    @classmethod
    def total_customers(cls):
        return cls.objects.count()


class RentalAgent(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        default='default_profiles/default.jpg',
        upload_to=agent_storage,
        null=True,
        blank=True,
        validators=[validate_image_extension, max_file_size_validator],
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user}'

    @classmethod
    def total_agents(cls):
        return cls.objects.count()


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.category_name


class Car(models.Model):
    car_image = models.ImageField(
        upload_to=car_storage,
        null=True,
        blank=True,
        validators=[validate_image_extension, max_file_size_validator],
    )
    model = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.model

    @classmethod
    def total_cars(cls):
        return cls.objects.count()

    @classmethod
    def available_cars(cls):
        return cls.objects.filter(available=True).count()


class Rental(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rental_start_date = models.DateTimeField()
    rental_end_date = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.customer} - {self.car}'

    @classmethod
    def total_revenue(cls):
        return cls.objects.aggregate(Sum('total_cost'))['total_cost__sum'] or 0

    @classmethod
    def total_bookings(cls):
        return cls.objects.count()


class Payment(models.Model):
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateTimeField(auto_now_add=True)  # Auto set on creation
    payment_slip = models.ImageField(
        upload_to=payment_storage,
        null=True,
        blank=True,
        validators=[validate_image_extension, max_file_size_validator],
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def delete(self, *args, **kwargs):
        # Delete payment slip when payment is deleted
        if self.payment_slip:
            self.payment_slip.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.rental} - {self.amount}'

    @classmethod
    def total_payments(cls):
        return cls.objects.aggregate(Sum('amount'))['amount__sum'] or 0
