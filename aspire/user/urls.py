from django.urls import path
from .views import RegisterView

urlpatterns = [
    # Api urls
    path("register/", RegisterView.as_view(), name="register"),
]
