from django.shortcuts import redirect

appname = "fatmmug_vms"


def index(request):
    """
    this function is designed specifically for replace the root url with vms_api root url.
    e.g. if user requests path localhost:8000, he will be redirected to localhost:8000/api/
    :param request:
    :return: redirect
    """
    return redirect("api_index")
