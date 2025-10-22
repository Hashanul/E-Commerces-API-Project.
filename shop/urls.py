from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UserViewSet, CustomerProfileViewSet, CategoryViewSet,
                    ProductViewSet, CartViewSet, CartItemViewSet, CheckoutViewSet,
                    OrderViewSet, OrderItemViewSet, PaymentViewSet)


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('profiles', CustomerProfileViewSet)
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register('cart-items', CartItemViewSet)
router.register('carts', CartViewSet)
router.register('checkouts', CheckoutViewSet)
router.register('orders', OrderViewSet)
router.register('order-items', OrderItemViewSet)
router.register('payments', PaymentViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
