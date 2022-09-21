from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('category', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('category/<int:category_pk>/item/', views.ItemCreateListView.as_view(), name='item-create-list'),
    path('category/<int:category_pk>/item/<int:pk>/',
         views.ItemRetrieveUpdateDestroyView.as_view(), name='item-retrieve-update-destroy'),
    path('category/<int:category_pk>/item/<int:item_pk>/order/', views.OrderCreateView.as_view(), name='order-create'),
    path('category/<int:category_pk>/item/<int:item_pk>/order/<int:pk>/',
         views.OrderRetrieveUpdateDestroyView.as_view(), name='order-retrieve-update-destroy'),
    path('order/', views.OrderListView.as_view(), name='order-list'),

]