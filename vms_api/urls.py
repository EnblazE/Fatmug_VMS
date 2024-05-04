from django.urls import path
from vms_api import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'vendors')
router.register(r'purchase_orders')
appname = "vms_api"
urlpatterns = [
    path('', views.index, name="api_index"),
]
