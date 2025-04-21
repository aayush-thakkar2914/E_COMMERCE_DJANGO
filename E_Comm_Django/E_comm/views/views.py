from ..models import Product, CartItem, Order, Cart
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone


def product_list(request):
    products = Product.objects.all()
    return render(request, 'E_comm/product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

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

    # ✅ Calculate total amount
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    # ✅ Create the order with total amount
    order = Order.objects.create(
        user=request.user,
        ordered_at=timezone.now(),
        total_amount=total_amount, # make sure this field exists in your Order model
        is_paid = True
    )

    # ✅ Associate cart items with the order (if you're using a relation)
    order.items.set(cart_items)
    order.save()

    # ✅ Mark current cart as ordered
    Cart.objects.filter(user=request.user, is_ordered=False).update(is_ordered=True)

    # ✅ Clear current cart items
    cart_items.delete()

    # ✅ Create a new cart (optional)
    Cart.objects.create(user=request.user, is_ordered=False)

    # ✅ Redirect to success page with order ID
    return redirect('order_success', order_id=order.id)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'E_comm/order_detail.html', {'order': order})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Get or create an active cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user, is_ordered=False)

    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')  # Adjust according to your cart page name
