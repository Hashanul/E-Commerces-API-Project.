from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import (CustomerProfile, Category, Product, Cart,
                     CartItem, Checkout, Order, OrderItem, Payment)
from .serializers import (UserSerializer, CustomerProfileSerializer,
                          CategorySerializer, ProductSerializer, CartSerializer,
                          CartItemSerializer, CheckoutSerializer, OrderItemSerializer,
                          PaymentSerializer)
from .utils import get_user_cart, get_guest_cart, merge_guest_cart_to_user


# 1. User --
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# 2. Customer Profile --
class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # শুধুমাত্র current logged-in user-এর profile দেখাবে
        return CustomerProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # profile create করার সময় current user assign করবে
        serializer.save(user=self.request.user)


# 3. Category --
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# 4. Product --
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer


# 5. Cart & CartItem --
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    # permission_classes = [permissions.AllowAny]  

    def get_permissions(self):
        # Allow anonymous users to create/list session-based carts
        if self.action in ['create', 'list']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]



class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_permissions(self):
        # Allow anonymous users to add/list cart items (use session-based cart)
        if self.action in ['create', 'list']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


    def get_cart(self):
        """Get the correct cart depending on login status"""
        if self.request.user.is_authenticated:
            merge_guest_cart_to_user(self.request)
            return get_user_cart(self.request)
        else:
            return get_guest_cart(self.request)

    def get_queryset(self):
        cart = self.get_cart()
        return cart.items.all()

    def perform_create(self, serializer):
        cart = self.get_cart()
        product = serializer.validated_data.get('product')

        # Check if item already exists in cart
        existing_item = cart.items.filter(product=product).first()
        if existing_item:
            existing_item.quantity += serializer.validated_data.get('quantity', 1)
            existing_item.save()
            return existing_item  # just update, no new create
        else:
            serializer.save(cart=cart)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 6. Checkout --
class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


# 7. Order & OrderItem
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


# 8. Payment --
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]




