from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
    path('insert', views.insert),
    path('update', views.update),
    path('delete', views.delete),

])