from django.db import models
from django.contrib.auth.models import User



class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}"
    
# 2 Category & Product

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Category: {self.name}"
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 3. Cart & CartItem

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"cart : {self.id} - {self.user.username}"
    
    @property
    def total_price(self):
        return sum(item.subtotal for item in self.self.items.all())
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return f"{self.product.price * self.quantity}"
    
    def __str__(self):
        return f"{self.quantity} X {self.product.name}"
    
# 4. Checkout
class Checkout(models.model):
    PAYMENT_METHODS = [
        ('bkash', 'Bkash'),
        ('card', 'Card'),
        ('cod', 'Cash On Delivery'),
    ]
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkouts')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='checkout')
    shipping_address = models.TextField()
    billing_adress = models.TextField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checkout : {self.id} - {self.user.username}"
    
# 5. Order & OrderItem
class Order(models.Model):
    STATUS_CHOICE = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    checkout = models.OneToOneField(Checkout, on_delete=models.CASCADE, related_name='order')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"Order : {self.id} - {self.user.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f" {self.Product.name} - ({self.quantity})"
    
# 6. Payment 
class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=Checkout.PAYMENT_METHODS)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment : {self.id} - {self.order.user.username}"



