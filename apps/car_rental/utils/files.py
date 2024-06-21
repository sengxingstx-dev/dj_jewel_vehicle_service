from django.core.exceptions import ValidationError
from django.core.files import File
from PIL import Image
from io import BytesIO

from dj_jewel_vehicle_service.settings.common import FILE_UPLOAD_MAX_MEMORY_SIZE

import os


def validate_image_extension(image):
    allowed_extensions = ['jpeg', 'jpg', 'png', 'gif']
    extension = image.name.split('.')[-1].lower()

    if extension not in allowed_extensions:
        raise ValidationError(
            "Invalid image format. Please upload a valid image file (JPG, JPEG, PNG, GIF)."
        )


# Calculate the maximum file size in bytes
# 2.5 MB (2.5 * 1024 * 1024 bytes)
def max_file_size_validator(value):
    max_size_byte = FILE_UPLOAD_MAX_MEMORY_SIZE
    max_size_mb = max_size_byte / (1024**2)

    # print('Greater or Not:', value.size > max_size_byte)
    # print('max_size_mb:', value.size / (1024**2))

    if value.size > max_size_byte:
        raise ValidationError(f'File size cannot exceed {max_size_mb} MB.')


def agent_storage(instance, filename):
    # Modify the file name as needed
    agent_id = instance.id
    if agent_id is None:
        # If the agent is new and doesn't have an ID yet, use a temporary identifier
        agent_id = "new_agent"
    ext = filename.split('.')[-1]  # Get the file extension
    new_filename = f'agent_{agent_id}_profile.{ext}'  # Customize the new file name
    return os.path.join('agent_profiles/', new_filename)


def customer_storage(instance, filename):
    # Modify the file name as needed
    customer_id = instance.id
    if customer_id is None:
        # If the customer is new and doesn't have an ID yet, use a temporary identifier
        customer_id = "new_customer"
    ext = filename.split('.')[-1]  # Get the file extension
    new_filename = f'customer_{customer_id}_profile.{ext}'  # Customize the new file name
    return os.path.join('customer_profiles/', new_filename)


def car_storage(instance, filename):
    car_id = instance.id
    if car_id is None:
        car_id = "new_car"
    ext = filename.split('.')[-1]
    new_filename = f'car_{car_id}_image.{ext}'
    return os.path.join('car_images/', new_filename)


def payment_storage(instance, filename):
    payment_id = instance.id
    # if payment_id is None:
    #     payment_id = "new_payment"
    ext = filename.split('.')[-1]
    new_filename = f'payment_slip_{payment_id}.{ext}'
    return os.path.join('payment_slips/', new_filename)


# def compress_image(self, image):
#     try:
#         # Open the image using Pillow
#         img = Image.open(image)

#         # Perform image compression or other processing here
#         # Example: Resizing the image to a specific size
#         img.thumbnail((400, 400))

#         # Save the processed image to a BytesIO buffer
#         output = BytesIO()
#         img.save(output, format='JPEG', quality=75)

#         # Rewind the buffer to the beginning
#         output.seek(0)

#         # Return the processed image
#         return output
#     except Exception as e:
#         # Handle any exceptions that may occur during image processing
#         raise ValidationError("Error processing the image.")


def compress_image(instance):
    # Compress the profile image when an instance is added or updated
    if hasattr(instance, 'profile_image') and instance.profile_image:
        try:
            with Image.open(instance.profile_image) as im:
                img_format = im.format

                # If image is JPEG, compress using JPEG format
                if img_format == 'JPEG':
                    im.thumbnail((400, 400))
                    im_io = BytesIO()
                    im.save(im_io, 'JPEG', quality=70)
                    new_image = File(im_io, name=instance.profile_image.name)

                # If image is PNG, compress using PNG format
                elif img_format == 'PNG':
                    im.thumbnail((400, 400))
                    im_io = BytesIO()
                    im.save(im_io, 'PNG', optimize=True)
                    new_image = File(im_io, name=instance.profile_image.name)

                # If image is neither JPEG nor PNG, raise an exception
                else:
                    raise Exception(f'Unsupported image format: {img_format}')

                # Assign the compressed image back to the instance's image attribute
                instance.profile_image = new_image
        except Exception as e:
            # Handle any exceptions that may occur during image processing
            raise ValidationError(f'Error processing the image. {str(e)}')

    # Compress the car image when an instance is added or updated
    elif hasattr(instance, 'car_image') and instance.car_image:
        try:
            with Image.open(instance.car_image) as im:
                img_format = im.format

                # If image is JPEG, compress using JPEG format
                if img_format == 'JPEG':
                    im.thumbnail((400, 400))
                    im_io = BytesIO()
                    im.save(im_io, 'JPEG', quality=70)
                    new_image = File(im_io, name=instance.car_image.name)

                # If image is PNG, compress using PNG format
                elif img_format == 'PNG':
                    im.thumbnail((400, 400))
                    im_io = BytesIO()
                    im.save(im_io, 'PNG', optimize=True)
                    new_image = File(im_io, name=instance.car_image.name)

                # If image is neither JPEG nor PNG, raise an exception
                else:
                    raise Exception(f'Unsupported image format: {img_format}')

                # Assign the compressed image back to the instance's image attribute
                instance.car_image = new_image
        except Exception as e:
            # Handle any exceptions that may occur during image processing
            raise ValidationError(f'Error processing the image. {str(e)}')

    # if instance.profile_image:
    #     pass

    # elif instance.car_image:
    #     pass
