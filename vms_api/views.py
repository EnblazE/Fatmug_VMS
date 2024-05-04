from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from vms_api.models import Vendor, Purchase_Order, Vendor_Performance
from vms_api.serializers import VendorModelSerializer, PurchaseOrderModelSerializer
from rest_framework import viewsets


# Create your views here.
@require_GET
def index(request):
    return HttpResponse("Hi")


class VendorModelViewset(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorModelSerializer


class PurchaseOrderViewset(viewsets.ModelViewSet):
    queryset = Purchase_Order.objects.all()
    serializer_class = PurchaseOrderModelSerializer
