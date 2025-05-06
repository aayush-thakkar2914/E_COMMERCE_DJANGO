from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .email_utils import send_order_status_email

# Product model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name

# Cart Item model
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

# Cart model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('PLACED', 'Order Placed'),
        ('ACCEPTED', 'Order Accepted'),
        ('SHIPPED', 'Order Shipped'),
        ('CITY', 'Arrived in Your City'),
        ('DELIVERED', 'Successfully Delivered'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(default=timezone.localtime)
    is_paid = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PLACED')
    
    # Fields to track status change timestamps
    accepted_at = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    arrived_city_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    def get_next_status(self):
        """Return the next expected status for this order"""
        current_status = self.status
        status_sequence = ['PLACED', 'ACCEPTED', 'SHIPPED', 'CITY', 'DELIVERED']
        
        try:
            current_index = status_sequence.index(current_status)
            if current_index < len(status_sequence) - 1:
                return status_sequence[current_index + 1]
        except ValueError:
            pass
        
        return None
    
    def get_expected_delivery_date(self):
        """Calculate the expected delivery date based on order date"""
        if self.ordered_at:
            return self.ordered_at + timedelta(days=3)
        return None
    
    def update_status(self):
        """Check if the order status should be updated based on time elapsed"""
        now = timezone.now()
        old_status = self.status
        
        # Order placed -> Order accepted (after 1 hour)
        if self.status == 'PLACED' and self.ordered_at and (now - self.ordered_at) > timedelta(hours=1):
            self.status = 'ACCEPTED'
            self.accepted_at = now
            self.save()
            # Send email notification
            send_order_status_email(self, old_status)
            
        # Order accepted -> Order shipped (after 1 day from acceptance)
        elif self.status == 'ACCEPTED' and self.accepted_at and (now - self.accepted_at) > timedelta(days=1):
            self.status = 'SHIPPED'
            self.shipped_at = now
            self.save()
            # Send email notification
            send_order_status_email(self, old_status)
            
        # Order shipped -> Arrived in city (after 1 day from shipping)
        elif self.status == 'SHIPPED' and self.shipped_at and (now - self.shipped_at) > timedelta(days=1):
            self.status = 'CITY'
            self.arrived_city_at = now
            self.save()
            # Send email notification
            send_order_status_email(self, old_status)
            
        # Arrived in city -> Delivered (after a few hours)
        elif self.status == 'CITY' and self.arrived_city_at and (now - self.arrived_city_at) > timedelta(hours=6):
            self.status = 'DELIVERED'
            self.delivered_at = now
            self.save()
            # Send email notification
            send_order_status_email(self, old_status)
    
    def get_status_percentage(self):
        """Calculate the percentage of order completion"""
        status_weights = {
            'PLACED': 0,
            'ACCEPTED': 25,
            'SHIPPED': 50,
            'CITY': 75,
            'DELIVERED': 100
        }
        return status_weights.get(self.status, 0)
    
    def save(self, *args, **kwargs):
        """Override save method to send email on status change"""
        # Check if this is a new order
        is_new = self.pk is None
        
        # If existing order, get the old status
        if not is_new:
            old_instance = Order.objects.get(pk=self.pk)
            old_status = old_instance.status
        else:
            old_status = None
        
        # Call the original save method
        super().save(*args, **kwargs)
        
        # Send email if status changed or new order
        if is_new or old_status != self.status:
            send_order_status_email(self, old_status)
    
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
# OrderItem model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_thumbnail = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.product.name}"