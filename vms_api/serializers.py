from rest_framework import serializers

from vms_api.models import Vendor, Purchase_Order

appname = "vms_api"


class VendorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ("name", "contact_details", "address", "vendor_code")


class PurchaseOrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase_Order
        exclude = ("quality_rating", "issue_date", "acknowledgment_date")
