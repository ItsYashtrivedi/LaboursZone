from django.urls import path

from . import views

urlpatterns = [
    path("register_home", views.register_home, name="register"),
    path("register_labour", views.register_labour, name="register_labour"),
    path("register_contractor", views.register_contractor, name="register-contractor"),
]