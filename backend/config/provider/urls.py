from django.urls import path

from .views import DeployView

app_name = "provider"

urlpatterns = [
    path("deploy/", DeployView.as_view(), name="home"),
]
