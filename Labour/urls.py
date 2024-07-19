from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("labour/job", views.job, name="job"),
    path("labour/labourslist", views.labourslist, name="labourslist"),
    path("labour/about", views.about, name="about"),
    path("labour/privacy", views.privacy, name="privacy"),
]