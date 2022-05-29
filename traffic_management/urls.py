"""
traffic_management URL Configuration
"""
from django.contrib import admin
from django.urls import path, include


from drf_spectacular.views import SpectacularRedocView, SpectacularAPIView

urlpatterns = [
    path("", SpectacularRedocView.as_view(), name="redoc"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("admin/", admin.site.urls),
    path("api/", include("roads.urls")),
]
