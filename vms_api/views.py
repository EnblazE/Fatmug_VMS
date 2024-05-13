from datetime import datetime
import plotly.graph_objects as go
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from vms_api.models import Vendor, Purchase_Order, Vendor_Performance
from django.db.models import Avg, ExpressionWrapper, F, IntegerField
from vms_api.serializers import VendorModelSerializer, PurchaseOrderModelSerializer
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

appname = 'vms_api'

DEFAULT_AUTH_CLASSES = [TokenAuthentication]  # by default the api uses TOKEN based authentication system
DEFAULT_PERM_CLASSES = [
    IsAuthenticated, ]  # by default the authentication works for ANY USER but to allow only admin users add IsAdminUser


# Create your views here.
@require_GET
def index(request):
    return render(request, "vms_api/index.html")


class VendorModelViewset(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorModelSerializer

    # authentication_classes = DEFAULT_AUTH_CLASSES
    # permission_classes = DEFAULT_PERM_CLASSES

    @property
    def default_response_headers(self):
        headers = viewsets.ModelViewSet.default_response_headers.fget(self)
        # headers['Authorization'] = 'Token ' + self.request.session['auth_token']
        return headers


class PurchaseOrderViewset(viewsets.ModelViewSet):
    queryset = Purchase_Order.objects.all()
    serializer_class = PurchaseOrderModelSerializer
    # authentication_classes = DEFAULT_AUTH_CLASSES
    # permission_classes = DEFAULT_PERM_CLASSES


class AcknowledgePurchaseOrder(View):
    """
    This view will validate if the purchase order exists and update the acknowledgment status of the purchase order
    and recalculate the average response time of the respective vendor.
    """

    # Message to reader:
    # Here in this view, the post method is used because it's handling the acknowledgment action,
    # which typically involves making changes to the server's data. While acknowledging a purchase order might seem
    # like a read-only action, it often involves updating the status of the purchase order in the database,
    # which is a modification operation.
    # So while it might be technically possible to implement acknowledgment using a GET request,
    # it's not recommended for the reasons mentioned above. Using a POST request is more aligned with
    # RESTful principles and ensures that the API behaves predictably and safely.
    def get(self, request, po_id):
        if po_id == 0 or po_id == None:
            # id has not been passed; returns to orders api page
            return redirect('po_api_endpoints-list')
        else:
            try:
                purchase_order = Purchase_Order.objects.get(id=po_id)
            except Purchase_Order.DoesNotExist:
                return JsonResponse({"error": "Purchase order does not exist.", "status": "status.HTTP_404_NOT_FOUND"})

            else:
                # 1. we update the acknowledgment date to current time
                current_full_time = datetime.now()
                purchase_order.acknowledgment_date = current_full_time
                purchase_order.save()

                # 2. now we calculate the average response time
                if purchase_order.issue_date > purchase_order.acknowledgment_date:
                    return JsonResponse({"message": "Failed to comply. Reason: Order has not been issued yet",
                                         "status": "status.HTTP_200_OK"}
                                        )
                else:
                    current_vendor = purchase_order.vendor
                    all_orders_from_vendor = current_vendor.vendor_po.all()
                    only_acknowledged_orders = all_orders_from_vendor.exclude(acknowledgment_date__isnull=True)
                    average_difference = only_acknowledged_orders.aggregate(
                        avg_difference=Avg(
                            ExpressionWrapper(
                                (F('acknowledgment_date') - F('issue_date')),
                                # Generally Avg function can't handle datatimefield hence we
                                # are converting the difference value into seconds (float)
                                output_field=IntegerField()
                            )
                        )
                    )['avg_difference'] or 0.0
                    average_difference /= 1000000  # the output from aggregation is combined integer of secs
                    # and microsecs e.g. output: 1770898501 (1770 secs, 898501 microsecs)
                    # so we need to convert it to (float) seconds before we save it

                    # 3. store the average in vendor object
                    current_vendor.average_response_time = float(average_difference)
                    current_vendor.save()
                    return JsonResponse(
                        {"message": f"Purchase order acknowledged successfully. Timestamp: {current_full_time}",
                         "status": "status.HTTP_200_OK"}
                    )


class VendorPerf(View):
    """
    This view is returned when
    """
    template_name = "vms_api/vendor_perf.html"

    # @method_decorator(require_GET)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request, vendor_id):
        """
        To use this method user needs to add vendor id manually to the url
        :param request: standard http request
        :param vendor_id: vendor id of the intended vendor
        :return: performance metrics page if vendor id is recognised
        """
        context = {}
        try:
            requested_vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            context["error"] = "Requested vendor does not exist. Please check the vendor id."
        else:
            context['vendor_data'] = requested_vendor
            self.take_metrics_snapshot(requested_vendor=requested_vendor)  # taking a snapshot
            graphs = PerfGraphs()
            context.update(graphs.get_context_data(vendor_itself=requested_vendor))
            
        return render(request, self.template_name, context)

    def take_metrics_snapshot(self, requested_vendor):
        """
        This function will run everytime user requests for vendor performance page and capture the current value
        of the vendor perf metrics and create an object of vendor_performance model in models.py
        """
        Vendor_Performance.objects.create(vendor=requested_vendor,
                                          date=datetime.now(),
                                          on_time_delivery_rate=requested_vendor.on_time_delivery_rate,
                                          quality_rating_avg=requested_vendor.quality_rating_avg,
                                          avg_response_time=requested_vendor.average_response_time,
                                          fulfillment_rate=requested_vendor.fulfillment_rate)


class PerfGraphs(TemplateView):
    """
    This view generates the plotly charts based on the vendor metrics data and returns as html
    """

    def get_context_data(self, vendor_itself, **kwargs):
        context = super(PerfGraphs, self).get_context_data(**kwargs)
        metrics_data_as_l = list(
            Vendor_Performance.objects.filter(vendor=vendor_itself).values_list("date", "on_time_delivery_rate",
                                                                                "quality_rating_avg",
                                                                                "avg_response_time",
                                                                                "fulfillment_rate"))
        print("full data:", *metrics_data_as_l, sep="\n")
        x = [t[0] for t in metrics_data_as_l]  # x-axis is same for all charts i.e. date of report

        # 1. plotting chart for on time delivery rate ------------------------------------------------------------------
        y = [t[1] for t in metrics_data_as_l]
        trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 10},
                            mode="lines", name='1st Trace')

        layout = go.Layout(title="On-Time Delivery", xaxis={'title': 'Report dates'}, yaxis={'title': 'No. of '
                                                                                                      'Deliveries'})
        figure = go.Figure(data=trace1, layout=layout)

        context['graph_on_time_delivery_rate'] = figure.to_html()

        # 2. plotting chart for average quality rating -----------------------------------------------------------------
        y = [t[2] for t in metrics_data_as_l]
        trace2 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 10},
                            mode="lines", name='2nd Trace')

        layout = go.Layout(title="Order Quality Rating(avg)", xaxis={'title': 'Report dates'},
                           yaxis={'title': 'Rating(between 0 to 5)'})
        figure = go.Figure(data=trace2, layout=layout)

        context['graph_quality_rating_avg'] = figure.to_html()

        # 3. plotting chart for average response time ------------------------------------------------------------------
        y = [t[3] for t in metrics_data_as_l]
        trace3 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 10},
                            mode="lines", name='3rd Trace')

        layout = go.Layout(title="Response Time(avg)", xaxis={'title': 'Report dates'}, yaxis={'title': 'Time in secs'})
        figure = go.Figure(data=trace3, layout=layout)

        context['graph_avg_response_time'] = figure.to_html()

        # 4. plotting chart for overall fulfillment rate ---------------------------------------------------------------
        y = metrics_data_as_l[4]
        trace4 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 10},
                            mode="lines", name='4th Trace')

        layout = go.Layout(title="Order Fulfillment Rate", xaxis={'title': 'Report dates'}, yaxis={'title': 'No. of '
                                                                                                            'Deliveries'
                                                                                                   })
        figure = go.Figure(data=trace4, layout=layout)

        context['graph_fulfillment_rate'] = figure.to_html()

        return context


class CustomLoginView(LoginView):
    template_name = 'vms_api/login.html'

    def form_valid(self, form, *args, **kwargs):
        super().form_valid(form)
        user = self.request.user
        token, created = Token.objects.get_or_create(user=user)
        self.request.session['auth_token'] = token.key
        return redirect("api_index")


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # Retrieve the authentication token from the session
        token_key = request.session.get('auth_token', None)
        if token_key:
            try:
                # Delete the token from the database
                token = Token.objects.get(key=token_key)
                token.delete()
            except Token.DoesNotExist:
                pass  # Token does not exist or has already been deleted

            # Clear the token from the session
            del request.session['auth_token']

        # Call Django's logout function to clear the user's session data
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return redirect("api_index")
    # return JsonResponse({'message': 'Logged out successfully'})
