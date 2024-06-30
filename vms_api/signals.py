from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from vms_api.models import Purchase_Order, Vendor


@receiver(post_save, sender=Purchase_Order)
def update_delivery_rate(sender, instance, created, **kwargs):
    """
    This post_save signal modifies the vendor object
    :param sender: Purchase_Order model which will send the signal upon saving
    :param instance: the PO object which created or being updated
    :param created: boolean value which tells if the instance is created or updated
    :param kwargs: non-required
    :return: None
    """
    if instance.status == "completed" or instance.quality_rating > 0.9:
        print("Information: a post_save signal triggered\nSender: ", sender, "\nInstance id: ", instance.id,
              "\Instance created: ", created, "kwargs: ", kwargs)
        """ Objective: first we modify the new on-time delivery rate """
        current_vendor = instance.vendor
        all_orders_from_vendor = current_vendor.vendor_po.all()
        only_completed_orders = all_orders_from_vendor.filter(status='completed')
        # calculate new delivery rate
        current_vendor.on_time_delivery_rate = only_completed_orders.filter(
            delivery_date__lte=datetime.now()).count() / all_orders_from_vendor.count()
        # Logic: Count the number of completed POs delivered on or before \
        # delivery_date and divide by the total number of completed POs for that vendor

        """ Objective: then we modify the fulfillment rate """
        current_vendor.fulfillment_rate = only_completed_orders.count() / all_orders_from_vendor.count()
        # Logic: Divide the number of successfully fulfilled POs (status 'completed' \
        # without issues) by the total number of POs issued to the vendor

        """ Object: now we calculate the avg vendor rating """
        orders_with_rating = all_orders_from_vendor.filter(quality_rating__gte=0.0)
        current_vendor.quality_rating_avg = orders_with_rating.aggregate(
            Avg("quality_rating", default=0.0))['quality_rating__avg']
        # Logic: Calculate the average of all quality_rating values for completed POs of the vendor.
        # I used Avg() on aggregate function to make it easy to implement and read

        # now we commit our update
        current_vendor.save()


from rest_framework.authtoken.models import Token


# we generate TOKEN when new user is created
@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    # if created and instance.is_superuser: # use this statement if only ADMIN is allowed to use the API
    if created:
        Token.objects.create(user=instance)
