from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.car_rental.models import RentalAgent, Customer


@receiver(post_delete, sender=RentalAgent)
def delete_user(sender, instance, **kwargs):
    # Automatically delete the associated user when the RentalAgent is deleted
    instance.user.delete()


@receiver(post_delete, sender=Customer)
def delete_user(sender, instance, **kwargs):
    # Automatically delete the associated user when the Customer is deleted
    instance.user.delete()
