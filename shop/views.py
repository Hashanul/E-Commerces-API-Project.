from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import (CustomerProfile, Category, Product, Cart,
                     CartItem, Checkout, Order, OrderItem, Payment)


