from django.urls import path

from . import api

urlpatterns = [
  path('',api.notifications,name='notifications'),
  # path('read/<uuid:pk>/',views.read_notification,name="read_notifications")
]