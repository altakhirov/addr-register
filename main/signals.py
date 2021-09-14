from django.db.models.signals import post_save
from django.dispatch import receiver

from main import models


@receiver(post_save, sender=models.House)
def create_private_house(sender, instance, created, **kwargs):
    if created:
        if not instance.with_flats:
            models.PrivateProperty.objects.create(
                house_id=instance.id
            )


@receiver(post_save, sender=models.Apartment)
def create_private_house_with_apartment(sender, instance, created, **kwargs):
    if created:
        models.PrivateProperty.objects.create(
            house_id=instance.house.id,
            apartment_id=instance.id
        )
