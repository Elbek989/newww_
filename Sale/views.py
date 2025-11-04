from rest_framework import generics, status, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Sale
from Sale.serializers import SaleCreateSerializer, SaleDetailSerializer


class SaleCreateView(generics.CreateAPIView):
    serializer_class = SaleCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Yangi sotuv yaratish (bir nechta mahsulot bilan)",
        request_body=SaleCreateSerializer,
        responses={201: SaleDetailSerializer}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        sale = serializer.save()
        response_serializer = SaleDetailSerializer(sale)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class SaleListView(generics.ListAPIView):
    queryset = Sale.objects.all().order_by('-date')
    serializer_class = SaleDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Foydalanuvchining barcha sotuvlari ro‘yxati",
        responses={200: SaleDetailSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return Sale.objects.filter(customer=user).order_by('-date')


class SaleDetailView(generics.RetrieveAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Sotuvni ID orqali ko‘rish",
        responses={200: SaleDetailSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CustomerSalesHistoryView(generics.GenericAPIView):
    serializer_class = SaleDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Customerning xaridlar tarixi",
        responses={200: SaleDetailSerializer(many=True)}
    )
    def get(self, request):
        user = request.user

        if not getattr(user, "is_customer", False):
            return Response(
                {"detail": "Faqat customer uchun ruxsat."},
                status=status.HTTP_403_FORBIDDEN
            )

        sales = Sale.objects.filter(customer=user).order_by('-date')

        if not sales.exists():
            return Response(
                {"detail": "Sizda hali xaridlar mavjud emas."},
                status=status.HTTP_200_OK
            )

        serializer = self.serializer_class(sales, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
