from ..models import Product, CartItem, Order, Cart, OrderItem, UserProfile, ProductImage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from ..forms import UserProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def product_list(request):
    products = Product.objects.all()
    return render(request, 'E_comm/product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # If the product has no images but has a main image, create a ProductImage from it
    if not hasattr(product, 'images') or not product.images.exists():
        if product.image:
            ProductImage.objects.create(
                product=product,
                image=product.image,
                is_thumbnail=True
            )

    if request.method == 'POST':    
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        return redirect('cart')

    return render(request, 'E_comm/product_detail.html', {'product': product})
@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'E_comm/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')
@login_required
def order_success(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'E_comm/order_success.html', {'order': order})

@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('cart')

    # Check if all products have sufficient stock before creating order
    for item in cart_items:
        if item.product.stock < item.quantity:
            messages.error(request, f"Sorry, only {item.product.stock} units of {item.product.name} available.")
            return redirect('cart')

    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    order = Order.objects.create(
        user=request.user,
        ordered_at=timezone.now(),
        total_amount=total_amount,
        is_paid=True
    )

    # Create order items from cart items and update product stock
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        
        # Update product stock
        item.product.stock -= item.quantity
        item.product.save()

    # Clean up cart
    cart_items.delete()
    Cart.objects.filter(user=request.user, is_ordered=False).update(is_ordered=True)
    Cart.objects.create(user=request.user, is_ordered=False)

    return redirect('order_success', order_id=order.id)



@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'E_comm/order_detail.html', {'order': order})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)   
    cart, created = Cart.objects.get_or_create(user=request.user, is_ordered=False)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')  # Adjust according to your cart page name

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    return render(request, 'E_comm/order_history.html', {'orders': orders})

@login_required
def profile_view(request):
    # Create profile if it doesn't exist
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('profile')
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the error below.')
    else:
        profile_form = UserProfileForm(instance=profile)
        password_form = PasswordChangeForm(user=request.user)
    
    return render(request, 'E_comm/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })



