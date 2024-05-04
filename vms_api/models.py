from django.core.validators import MinValueValidator
from django.db import models

"""
These models form the backbone of the Vendor Management System, enabling
comprehensive tracking and analysis of vendor performance over time. The performance
metrics are updated based on interactions recorded in the Purchase Order mode
"""
appname = "vms_api"


# Create your models here.

class Vendor(models.Model):
    """
    This model stores essential information about each vendor and their performance metrics
    """

    def __int__(self):
        pass

    def __del__(self):
        pass

    def __str__(self):
        return f"{self.name}(ID: {self.id}, Code: {self.vendor_code})"

    # all relevant fields
    name = models.CharField(max_length=150, blank=False, null=False, validators=[], help_text="Vendor Name in full")
    contact_details = models.TextField(max_length=1000, blank=False, null=False,
                                       help_text="Vendor contact information")
    address = models.TextField(max_length=1000, blank=False, null=False, help_text="Vendor Official address in "
                                                                                   "full")
    vendor_code = models.CharField(max_length=50, blank=False, null=False, unique=True, help_text="Unique Vendor code")
    on_time_delivery_rate = models.FloatField(blank=True, null=False, default=0.0)
    quality_rating_avg = models.FloatField(blank=True, null=False, default=0.0)
    average_response_time = models.FloatField(blank=True, null=False, default=0.0)
    fulfillment_rate = models.FloatField(blank=True, null=False, default=0.0)


def random_issue_date():
    """
    this function returns current date with added minutes from current time
    :return:
    """
    import random
    import datetime
    current_date_and_time = datetime.datetime.now()

    # Using timedelta() function to increase minutes
    added_minutes = datetime.timedelta(minutes=random.randint(10, 70))  # random minutes between 10 and 70
    new_time = current_date_and_time + added_minutes
    return new_time


class Purchase_Order(models.Model):
    """
    This model captures the details of each purchase order and is used to calculate various
performance metrics
    """

    def __init__(self):
        pass

    def __del__(self):
        pass

    def __str__(self):
        return f"{self.po_number}"

    # all relevant fields
    po_number = models.CharField(max_length=50, blank=False, null=False, unique=True,
                                 help_text="Unique number identifying the PO")
    vendor = models.ForeignKey(Vendor, related_name="vendor_po", blank=False, null=False, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True, blank=True, null=False)
    delivery_date = models.DateTimeField(blank=False, null=False)
    items = models.JSONField(blank=False, null=False)
    quantity = models.IntegerField(blank=False, null=True, validators=[MinValueValidator(1)])
    status = models.CharField(choices=(
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("canceled", "Canceled")
    ), blank=True, null=False, default="pending", max_length=10)
    quality_rating = models.FloatField(blank=True, null=True)
    issue_date = models.DateTimeField(blank=True, null=False, default=random_issue_date())
    acknowledgment_date = models.DateTimeField(blank=True, null=True)  # this field will be updated automatically


class Vendor_Performance(models.Model):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def __str__(self):
        pass

    # all relevant fields
    vendor = models.ForeignKey(Vendor, related_name="vendor_perf", related_query_name="vendor",
                               on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="Modified date", auto_now_add=True, blank=True, null=False)
    on_time_delivery_rate = models.FloatField(verbose_name="Vendor on-time delivery rate", blank=True, null=False,
                                              default=0.0)
    quality_rating_avg = models.FloatField(verbose_name="Vendor average rating for orders", blank=True, null=False,
                                           default=0.0)
    avg_response_time = models.FloatField(verbose_name="Vendor average response time for PO acknowledgment", blank=True,
                                          null=False,
                                          default=0.0)
    fulfillment_rate = models.FloatField(verbose_name="Vendor PO completion rate", blank=True, null=False, default=0.0)
