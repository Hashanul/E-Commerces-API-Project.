from rest_framework import serializers
from django.contrib.auth.models import User
from .models import(
    CustomerProfile, Category, Product, Cart, CartItem, Checkout, Order, OrderItem, Payment
)

# User Serializer
