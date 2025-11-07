from django.urls import path
from .views import CartListView, CartAddItemView, CartItemRemoveView, CartUpdateItemView

urlpatterns = [
    path('', CartListView.as_view(), name='cart-detail'),
    path('add-item/', CartAddItemView.as_view(), name='cart-add-item'),
    path('remove-item/<int:item_id>/', CartItemRemoveView.as_view(), name='cart-remove-item'),
    path('cart/update-item/<int:item_id>/', CartUpdateItemView.as_view(), name='cart-update-item'),
]
