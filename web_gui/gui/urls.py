from django.urls import path
from gui import views


urlpatterns = [
    path('', views.index, name="index"),
]