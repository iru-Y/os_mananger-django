from django.contrib import admin
from django.urls import path, include

api_prefix = 'api/v1'


urlpatterns = [
    path('admin/', admin.site.urls),
    path(api_prefix, include('customers.urls')),
]
