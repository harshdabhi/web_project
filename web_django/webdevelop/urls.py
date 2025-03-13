from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Factory Machinery Status & Repair Tracking API",
        default_version='v1',
        description="""
API for tracking factory machinery status, warnings, and faults.

## Authentication
This API uses token-based authentication. To use the API:
1. Register a new user: POST /api/auth/register/
2. Login to get a token: POST /api/auth/token/
3. Click "Authorize" button and in the Bearer (apiKey) put as field : `Token your_token_here`
4. Now you can use the API in the swagger UI
        """,
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[
        re_path(r'^api/', include('myapp.api_urls')),
    ],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("myapp.urls")),
    path("api/", include("myapp.api_urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
