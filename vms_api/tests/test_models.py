import json
import uuid
from datetime import datetime

from django.forms import model_to_dict
from django.test import TestCase

from vms_api.models import Vendor, Purchase_Order, Vendor_Performance


class DefaultTestCase(TestCase):
    """
    This test class will test creating three types of models available in the project
    - Vendor, Purchase_Order, Performance_Metrics
    """

    def setUp(self) -> None:
        """
        Populating with random data for corresponding model classes
        :return: None
        """
        # required fields for Vendor model
        self.name = "Oscar Borne"  # switch with your own
        self.contact_details = "Phone: 8061285676, Email: oborne@email.com"  # replace with your own
        self.address = "127 Grand Heron Drive, Panama City FL 32407"  # replace with your own
        self.vendor_code = str(uuid.uuid4())  # a random 36 digit uuid string

        # non-required fields for Vendor model
        self.on_time_delivery_rate: float
        self.quality_rating_avg: float
        self.average_response_time: float
        self.fulfill_rate: float

        # required fields for Purchase_Order model
        self.po_number = str(uuid.uuid4())  # a random 36 digit uuid string
        self.vendor: Vendor  # will be assigned when first test is run
        self.delivery_date = datetime(year=2024, month=8, day=12)
        self.items = json.dumps({"item1": "Eclair", "item2": "Milk-bread", "item3": "Noodle", "item4": "Banana"})
        self.quantity = 10
        self.quality_rating = 3.4

        # non-required fields for Purchase_Order model
        self.order_date: datetime  # auto populated by model
        self.status: str
        self.issue_date: datetime  # auto populated by model
        self.acknowledgment_date: datetime

        # required fields for Vendor_Performance model
        self.vendor: Vendor
        self.on_time_delivery_rate = 23
        self.quality_rating_avg = 2.5
        self.avg_response_time = 234
        self.fulfillment_rate = 124234
        # required fields for Vendor_Performance model
        self.date: datetime

        # utilities

    def test_create_dummies(self):
        """
        Objective: Creates a vendor model dummy object and prints the saved data to console
        :return: None
        """
        # We will start with a <class Vendor> object creation
        new_vendor = Vendor.objects.create(name=self.name,
                                           contact_details=self.contact_details,
                                           address=self.address,
                                           vendor_code=self.vendor_code)
        # We are checking here if the created object is in fact instance of the intended class otherwise prints error
        self.assertIsInstance(new_vendor, Vendor, "Created object is not of <class Vendor>")

        # Now we create two objects with new_vendor object of <class Purchase_Order> and <class Vendor_Performance>
        # respectively
        self.create_po(new_vendor)
        self.create_pm(new_vendor)

    def create_po(self, vendor):
        """
        Objective: Creates a purchase order dummy object and prints the saved object to console
        Note: field order_date won't show in output as it's a read_only field
        :return: None
        """
        new_po = Purchase_Order.objects.create(po_number=self.po_number,
                                               vendor=vendor,
                                               delivery_date=self.delivery_date,
                                               items=self.items,
                                               quantity=self.quantity,
                                               quality_rating=self.quality_rating)

        self.assertIsInstance(new_po, Purchase_Order, "Created object is not of <class Purchase_Order>")

    def create_pm(self, vendor):
        """
        Objective: Creates a vendor performance dummy object which is tightly depended on vendor object, but we create a
        standalone object here and prints the saved object to console
        Note: field date won't show in output as it's a read_only field

        :return: None
        """
        new_pm = Vendor_Performance.objects.create(vendor=vendor,
                                                   on_time_delivery_rate=self.on_time_delivery_rate,
                                                   quality_rating_avg=self.quality_rating_avg,
                                                   avg_response_time=self.avg_response_time,
                                                   fulfillment_rate=self.fulfillment_rate)

        self.assertIsInstance(new_pm, Vendor_Performance, "Created object is not of <class Vendor_Performance>")
