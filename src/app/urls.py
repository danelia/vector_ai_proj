from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
    # /continent
    path('continent', views.ContinentViewSet.as_view({
        'post' : 'create',
    })),
    path('continent/<int:entry_id>', views.ContinentViewSet.as_view({
        'put' : 'update',
        'delete' : 'delete',
    })),

    # /country
    path('country', views.CountryViewSet.as_view({
        'post' : 'create',
    })),
    path('country/<int:entry_id>', views.CountryViewSet.as_view({
        'put' : 'update',
        'delete' : 'delete',
    })),

    # /city
    path('city', views.CityViewSet.as_view({
        'post' : 'create',
    })),
    path('city/<int:entry_id>', views.CityViewSet.as_view({
        'put' : 'update',
        'delete' : 'delete',
    })),

    # for checking task
    path('check_task/<str:task_id>', views.check_task),

])