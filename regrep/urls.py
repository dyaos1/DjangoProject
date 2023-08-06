from django.contrib import
from django.urls import include, path
from regrep import views

urlpatterns = [
    path("/", views.load_report, name="load"),
]