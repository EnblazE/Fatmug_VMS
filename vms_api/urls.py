from django.urls import path, include
from vms_api import views
from fatmug_vms import views as fatmug_vms_views
from rest_framework import routers
# from rest_framework.authtoken.views import obtain_auth_token
from vms_api import auth
from vms_api.views import CustomLoginView, CustomLogoutView

# registering api endpoints
router = routers.DefaultRouter()
router.register(r'vendors', views.VendorModelViewset, basename="vendors_api_endpoints")
router.register(r'purchase_orders', views.PurchaseOrderViewset, basename="po_api_endpoints")

appname = "vms_api"

urlpatterns = [
    path('index', views.index, name="api_index"),
    path('', include(router.urls)),
    path(r'$', fatmug_vms_views.index, name=""),
    path('auth/login/', CustomLoginView.as_view(), name='custom_login'),
    path('auth/logout/', CustomLogoutView.as_view(), name='custom_logout'),
    path('gettoken', auth.CustomAuthToken.as_view(), name="get_auth_token"),
    # if required manually generate authentication token
    path('purchase_orders/<int:po_id>/acknowledge/', views.AcknowledgePurchaseOrder.as_view(),
         name="acknowledge_order"),
    path('vendors/<int:vendor_id>/performance', views.VendorPerf.as_view(), name="vendor_perf"),
]
