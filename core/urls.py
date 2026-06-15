"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view

from .docs import SwaggerUIView

schema_view = get_schema_view(
    title=settings.SCHEMA_TITLE,
    description=settings.SCHEMA_DESCRIPTION,
    version=settings.SCHEMA_VERSION,
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", schema_view, name="api-schema"),
    path("api/docs/", SwaggerUIView.as_view(), name="api-docs"),
    path("", RedirectView.as_view(url="/api/docs/", permanent=False), name="root-redirect"),
    path("brain/", include("brain.routes")),
    path("", include("api_gateway.urls")),
    path("", include("heart.routes")),
]
