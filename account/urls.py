from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('register/<str:is_sender>/', views.RegisterView.as_view()),

]