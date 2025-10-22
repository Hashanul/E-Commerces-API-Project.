from django.contrib import admin
from .models import (
    CustomerProfile, Category, Product, Cart, CartItem,
    Checkout, Order, OrderItem, Payment
)

admin.site.register(CustomerProfile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Checkout)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)























# from django.contrib import admin
# from .models import (
#     CustomerProfile, Category, Product, Cart, CartItem, Checkout, Order, OrderItem, Payment
# )


# # Customer Profile
# @admin.register(CustomerProfile)
# class CustomerProfileAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'phone', 'city', 'country']
#     search_fields = ['user__username', 'phone', 'city', 'country']


# # Category
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'description']
#     search_fields = ['name']
#     ordering = ['name']


# # Product
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'category', 'price', 'stock', 'available', 'created_at']
#     list_filter = ['available', 'category']
#     search_fields = ['name', 'category__name', 'description']
#     prepopulated_fields = {'slug' : ['name']}
#     list_editable = ('price', 'stock', 'available')
#     ordering = ['-created_at']


# # Cart & CartItem
# class CartItemInline(admin.TabularInline):   # ???
#     model = CartItem
#     extra = 0


# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'created_at', 'updated_at', 'total_price']
#     inlines = [CartItemInline]
#     search_fields = ['user__username']
#     ordering = ['-created_at']

# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ['id', 'product', 'product_id', 'quantity', 'subtotal']
#     search_fields = ['cartitem__id', 'product_name']


# # Checkout
# @admin.register(Checkout)
# class CheckoutAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'payment_method', 'total_price', 'status', 'created_at']
#     list_filter = ['payment_method', 'status']
#     search_fields = ['user__username', 'payment_method', 'status']
#     ordering = ['-created_at',]


# # Order & OrderItem
# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'checkout', 'total_price', 'status', 'created_at']
#     list_filter = ['status',]
#     search_fields = ['user__username', 'checkout__id']
#     inlines = [OrderItemInline]
#     ordering = ['-created_at',]


# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['id', 'order', 'product', 'quantity', 'price']
#     search_fields = ['order__id', 'product_name']


# # Payment
# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'order', 'payment_method', 'payment_status', 'transaction_id', 'paid_at']