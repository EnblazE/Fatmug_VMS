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
                  "acknowledge_button")

    def get_acknowledge_button(self, obj):
        request = self.context.get('request')
        if request and request.method == 'GET':
            acknowledge_url = request.build_absolute_uri(
                reverse('acknowledge-purchase-order', args={'po_id': obj.id}))
            return f'<a href="{acknowledge_url}" target="_blank"><button>Acknowledge</button></a>'
        return None
