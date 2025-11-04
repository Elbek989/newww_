from django.urls import path
from products.views import *

urlpatterns = [
    # Products
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # Categories
    path('categories/', ProductCategoryView.as_view(), name='category-list'),
    path('categories/create/', ProductCategorycreate.as_view(), name='category-create'),
]
