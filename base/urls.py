from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("downloadfile", views.downloadfile, name = "download"),
    path("downloadfile/<res>/", views.downloadfile, name = "download"),
]
