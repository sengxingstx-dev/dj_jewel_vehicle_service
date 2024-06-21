from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Rental, Payment


@receiver(post_save, sender=Rental)
def update_car_status_on_booking(sender, instance, created, **kwargs):
    if created:
        print('Triggered Rental signal....')
        # Calculate the total price
        nights = (instance.rental_end_date - instance.rental_start_date).days
        car = instance.car
        instance.total_cost = nights * car.price
        instance.save()

        # Set the car available to False
        car.available = False
        car.save()


@receiver(post_delete, sender=Rental)
def update_car_status_on_checkout(sender, instance, **kwargs):
    print('Triggered Rental post_delete...')
    car = instance.car
    car.available = True
    car.save()


@receiver(post_delete, sender=Payment)
def delete_payment(sender, instance, **kwargs):
    print('Triggered Payment post_delete...')
    if instance.payment_slip:
        instance.payment_slip.delete(save=False)
