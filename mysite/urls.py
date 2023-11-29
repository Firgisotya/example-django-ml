
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('OC1/', include('OC1.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
