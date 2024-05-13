Fatmug Vendor Management System is a Django-based web application made for Fatmug as part of recruitment process
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
This assignment tests my ability to create a functional Django-based system for vendor
management, integrating aspects of data handling, API development, and basic performance
metric calculations.
Vendor Management system lets you create Vendors through RESTful browsable API and also Purchase Orders for each vendor.
It also provides an exclusive Vendor performance metric system which works on real-time data and presents us with
various metrics using
modern interative charts.

__Instructions:__

1. Clone the repo using Git or GitHub cli

   ```gh repo clone EnblazE/Fatmug_VMS```

2. Open the project folder in your console and activate virtual env
    - For Windows:
      ```.\venv\Scripts\activate```
    - For Linux or Mac:
      ```./venv/bin/activate```
3. Now run the Django server (You need Python 3.11.6+)

   ```python manage.py runserver``` or
   ```python3 manage.py runserver```
4. Open web browser and open http://127.0.0.1:8000 or use curl

   ```curl http://127.0.0.1:8000```

By default, you will be redirected the API index page which will give you the sitemap of the site.
To access the API you need to log in to the system.

While you are authenticated you can perform CRUD operations on inbuild models
through browsable API powered by Django Rest Framework.
You also can generate performance metrics of any vendor registered in the system
by going to ``/api/vendors/{vendor_id}/performance`` with ``{vendor_id}`` replaced with desired vendor id.

**API Endpoints:**

* (Vendor specific):

  ``POST/api/vendors/`` - Create a new vendor.

  ``GET/api/vendors/`` - List all vendors.

  ``GET/api/vendors/{vendor_id}/`` - Retrieve a specific vendor's details.

  ``PUT/api/vendors/{vendor_id}/`` - Update a vendor's details.

  ``DELETE/api/vendors/{vendor_id}/`` - Delete a vendor.


* (Purchase order specific):

  ``POST/api/purchase_orders/`` - Create a purchase order.
  ``GET/api/purchase_orders/`` - List all purchase orders with an option to filter by
  vendor.

  ``GET/api/purchase_orders/{po_id}/`` - Retrieve details of a specific purchase order.

  ``PUT/api/purchase_orders/{po_id}/`` - Update a purchase order.

  ``DELETE/api/purchase_orders/{po_id}/`` - Delete a purchase order.

Note: Vendor performance model does not any API presentation as it will automatically generate when you go to it's
corresponding
url: ``/api/vendors/{vendor_id}/performance`` and it uses [Plotly](https://plotly.com/python/) to generate the graphs
based on the historical data of the desired vendor. We have chosen Plotly as facilates us with modern, industry-grade
and interatice graph generation.

**Authentication:**

Our authentication system is developed using simplicity of Django's in build authorization system but grants superior
security of Token based authentication mechanism.
Go to ``/auth/login/`` page to start the login procedure. When you are successfully logged in you will redirected to the
homepage.
To logout from the system you need go ``auth/logout/``.

To generate token for token-based entry make a POST request through any http client
``POST http://127.0.0.1:8000/gettoken/ username="amanlalwani" password="aman"``
e.g. [curl](https://curl.se/)
``curl -X POST -d "username=amanlalwani&password=aman" http://127.0.0.1:8000/gettoken/``

Then you need to attach the token in request header when accessing the API pages
like this: ``http://127.0.0.1:8000/studentapi/ 'Authorization:Token d96d3fbd5e0b0dd4cdf681aee8c133f0d6b61e24'``
If you use
curl then do like this:
``curl -X GET -H "Authorization: Token d96d3fbd5e0b0dd4cdf681aee8c133f0d6b61e24" http://127.0.0.1:8000/studentapi/``

Note: To create new user/admin you need to visit Django's default admin page at
``http://127.0.0.1:8000/admin``

**Testing:**

Currently, a basic testing suite is designed and it works as intended. You can run these predefined tests by
``python manage.py test``. This command is will run all the test modules one by one. You can modify the test suite by
visitng each ``test_*.py``
files can be found under ``../vms_api/tests/``. Each file has it's own setUp function defined and run tests using
[django.unittest](https://docs.python.org/3/library/unittest.html#module-unittest)
and [rest_framework.test](https://www.django-rest-framework.org/api-guide/testing/) modules.
Each test_*.py file is intended to perform a specific type of test and named accordingly, for example, test_api.py is
made to test only API related tests which checks object creation using rest framework api.