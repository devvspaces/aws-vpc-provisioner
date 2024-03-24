from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg.generators import OpenAPISchemaGenerator
from django.conf import settings
from django.conf.urls.static import static


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


base_schema_view = get_schema_view(
    openapi.Info(
        title="Terraform VPC Provider",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=BothHttpAndHttpsSchemaGenerator
)


doc_urls = [
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("api/v1/", include("provider.urls")),
    path(
        'docs/',
        base_schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
