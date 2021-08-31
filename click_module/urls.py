from django.urls import path
from . import views

urlpatterns = [
    path('prepare', views.prepare, name='prepare'),
    path('complete', views.complete, name='complete'),
    path('service/<service_type>', views.service, name='service')
]
