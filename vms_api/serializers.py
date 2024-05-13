from rest_framework import serializers
from rest_framework.reverse import reverse

from vms_api.models import Vendor, Purchase_Order

appname = "vms_api"


class VendorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ("name", "contact_details", "address", "vendor_code")


class PurchaseOrderModelSerializer(serializers.ModelSerializer):
    acknowledge_button = serializers.SerializerMethodField()

    class Meta:
        model = Purchase_Order
        # exclude = ("quality_rating", "issue_date", "acknowledgment_date")
        fields = ("po_number", "vendor", "delivery_date", "items", "quantity", "status", "quality_rating", "issue_date",
                  "acknowledge_url")

    def get_acknowledge_url(self, obj):
        request = self.context.get('request')
        if request and request.method == 'GET':
            acknowledge_url = request.build_absolute_uri(
                reverse('acknowledge_order', kwargs={'po_id': obj.id}))
            return acknowledge_url
        return None
