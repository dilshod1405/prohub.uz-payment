from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Payment Service API of prohub.uz learning platform",
        default_version='v1',
        description="Payment Service API of prohub.uz learning platform",
        contact=openapi.Contact(email="www.prohub.uz@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticatedOrReadOnly],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/', include('transactions.urls')),
    path('pay/payme/', include('transactions.payme.urls')),
    path('pay/click/', include('transactions.click.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    path('docs/', schema_view.with_ui('swagger',cache_timeout=0),name='swagger-docs'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),