from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('login/', LoginView.as_view(), name='loginToken'),
    path('product/', include(router.urls)),  # ← shu yerda "/" bo‘lishi kerak
]
