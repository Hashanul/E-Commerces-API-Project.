from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import (CustomerProfile, Category, Product, Cart,
                     CartItem, Checkout, Order, OrderItem, Payment)
from .serializers import (UserSerializer, CustomerProfileSerializer,
                          CategorySerializer, ProductSerializer, CartSerializer,
                          CartItemSerializer, CheckoutSerializer, OrderItemSerializer,
                          PaymentSerializer)


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

    def get_queryset(self):
        user = self.request.user if self.request.user.is_authenticated else None
        if user:
            return Cart.objects.filter(user=user)
        else:
            session_id = self.request.session.session_key
            if not session_id:
                self.request.session.create()
            return Cart.objects.filter(session_id=session_id)
    
    def get_or_create_cart(self, request):
        user = request.user if request.user.is_authenticated else None 
        if user:
            cart, _ = Cart.objects.get_or_create(user=user)
        else:
            if not request.session.session_key:
                request.session.create()
            session_id = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_id=session_id, user=None)
        return cart
    
    def create(self, request, *args, **kwargs):
        """Add product to cart"""
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        cart = self.get_or_create_cart(request)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        """Get current user's/session's cart"""
        cart = self.get_or_create_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Clear all items from current cart"""
        cart = self.get_or_create_cart(request)
        cart.items.all().delete()
        return Response({"message": "Cart cleared"}, status=204)  


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    # permission_classes = [permissions.IsAuthenticated]  


    def get_queryset(self):
        request = self.request
        if request.user.is_authenticated:
            return CartItem.objects.filter(cart__user=self.request.user)
        else:
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
            return CartItem.objects.filter(cart__session_id=session_id)
    
    def perform_create(self, serializer):
        cart = None
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
        else:
            if not self.request.session.session_key:
                self.request.session.create()
            session_id = self.request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_id=session_id, user=None)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)

        # Check if the product already exists in the cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            # If it exists, just increment the quantity
            cart_item.quantity += quantity
            cart_item.save()


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





