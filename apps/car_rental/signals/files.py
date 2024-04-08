from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from ..utils.files import compress_image
from ..models import RentalAgent, Customer, Car


def process_and_compress_image(instance):
    if instance.pk:
        try:
            old_instance = instance.__class__.objects.get(pk=instance.pk)

            # Delete the old profile image when a new profile image is provided
            if hasattr(instance, 'profile_image') and instance.profile_image:
                if (
                    hasattr(old_instance, 'profile_image')
                    and old_instance.profile_image.name == 'default_profiles/default.jpg'
                ):
                    compress_image(instance)
                elif (
                    hasattr(old_instance, 'profile_image')
                    and instance.profile_image.name != old_instance.profile_image.name
                ):
                    if old_instance.profile_image:
                        old_instance.profile_image.delete(save=False)

            # Delete the old car image when a new car image is provided
            elif hasattr(instance, 'car_image') and instance.car_image:
                if (
                    hasattr(old_instance, 'car_image')
                    and instance.car_image.name != old_instance.car_image.name
                ):
                    if old_instance.car_image:
                        old_instance.car_image.delete(save=False)

            # Check if the new image is different from the old one
            new_image_name = (
                instance.profile_image.name
                if hasattr(instance, 'profile_image')
                else instance.car_image.name
            )
            old_image_name = (
                old_instance.profile_image.name
                if hasattr(old_instance, 'profile_image')
                else old_instance.car_image.name
            )

            if new_image_name != old_image_name:
                # Process and compress the cover image
                compress_image(instance)

        except instance.__class__.DoesNotExist:
            raise ValidationError('The instance does not exist.')


@receiver(pre_save)
def process_image_on_save(sender, instance, **kwargs):
    # Check if the sender is either RentalAgent, Customer or Car
    if sender in [RentalAgent, Customer, Car]:
        process_and_compress_image(instance)


@receiver(pre_delete)
def delete_image_on_delete(sender, instance, **kwargs):
    # Check if the sender is either RentalAgent or Customer or Car
    if sender in [RentalAgent, Customer, Car]:
        # Delete the cover image when an instance is deleted
        # if instance.profile_image:
        #     instance.profile_image.delete(save=False)

        # elif instance.car_image:
        #     instance.car_image.delete(save=False)

        # Delete the old profile image when an instance is added or updated
        if hasattr(instance, 'profile_image') and instance.profile_image:
            instance.profile_image.delete(save=False)

        # Delete the old car image when an instance is added or updated
        elif hasattr(instance, 'car_image') and instance.car_image:
            instance.car_image.delete(save=False)
