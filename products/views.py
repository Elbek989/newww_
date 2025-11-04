from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from rest_framework.viewsets import ModelViewSet

from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCategorySerializer
from .make_token import get_user_token_from_serializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user

        if not user.is_staff and not getattr(user, 'is_seller', False):
            return Response(
                {"detail": "Faqat seller yoki admin mahsulot qo‘sha oladi."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().create(request, *args, **kwargs)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []


class ProductCategoryView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = []


class ProductCategorycreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request, *args, **kwargs):
        user = request.user

        if not user.is_staff and not getattr(user, 'is_seller', False):
            return Response(
                {"detail": "Faqat seller yoki admin mahsulot_cat qo‘sha oladi."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().create(request, *args, **kwargs)