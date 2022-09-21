from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, \
    get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from .models import Category, Item, Order
from .serializers import CategorySerializer, ItemSerializer, OrderSerializer
from account.models import Profile
from .permissions import CategoryPermission, ItemPermission, OrderPermission


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (CategoryPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class ItemView:
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (ItemPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class ItemCreateListView(ItemView, ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile, category=Category.objects.get(id=self.kwargs["category_pk"]))

    def get_queryset(self):
        return self.queryset.filter(category=self.kwargs['category_pk'])


class ItemRetrieveUpdateDestroyView(ItemView, RetrieveUpdateDestroyAPIView):
    pass


class OrderView:
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class OrderCreateView(OrderView, CreateAPIView):
    def create(self, request, *args, **kwargs):
        order = Order.objects.filter(profile=request.user.profile, item__id=kwargs["item_pk"]).first()
        if order:
            serializer = self.get_serializer(order, data=request.data, partial=True)
            this_status = status.HTTP_200_OK
        else:
            serializer = self.get_serializer(data=request.data)
            this_status = status.HTTP_201_CREATED
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=this_status, headers=headers)

    def perform_create(self, serializer):
        item = get_object_or_404(Item, id=self.kwargs["item_pk"])
        serializer.save(profile=self.request.user.profile, item=item)


class OrderListView(OrderView, ListAPIView):
    def get_queryset(self):
        return self.queryset.filter(profile=self.request.user.profile)


class OrderRetrieveUpdateDestroyView(OrderView, RetrieveUpdateDestroyAPIView):
    pass
