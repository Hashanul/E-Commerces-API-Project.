from rest_framework import serializers
from django.contrib.auth.models import User
from .models import(
    CustomerProfile, Category, Product, Cart, CartItem, Checkout, Order, OrderItem, Payment
)

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# CustomerProfile Serializer
class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)

    class Meta:
        model = CustomerProfile
        fields = '__all__'


# Category & Product
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    Category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


# Cart & CartItem
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'subtotal']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()
    total_items = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'total_items' ]

class CheckoutSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    cart = CartSerializer(read_only = True)

    class Meta:
        model = Checkout
        fields = '__all__'


# Order & OrderItem
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    checkout = CheckoutSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'checkout', 'items', 'total_price', 'status', 'created_at', 'updated_at']

# Payment
class PaymentSerializer(serializers.ModelSerializer):
    order = OrderItemSerializer(read_only = True)

    class Meta:
        model = Payment
        fields = "__all__"