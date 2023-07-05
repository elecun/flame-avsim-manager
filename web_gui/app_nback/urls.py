from django.urls import path
from app_nback import views


urlpatterns = [
    path('', views.index, name="index"),
]