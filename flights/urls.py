from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:ID>", views.flight, name="flight"),
    path("<int:ID>/book", views.book, name="book")
]
