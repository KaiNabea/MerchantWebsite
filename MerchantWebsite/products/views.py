<<<<<<< HEAD
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Products, Cart, CartItem

# Create your views here.
def product_list(request):
    products = Products.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products/product_list.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.filter(id='cart_id').first()
            if not cart:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    cart_item, created = CartItem.objects.get_or_create(
        cart = cart,
        product = product,
        defaults = {'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.product} added to cart.")
    return redirect('product_list')

def view_cart(request):
    cart = None
    cart_items = []
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()
    if cart:
        cart_items = cart.items.all()
    context = {
        'cart': cart,
        'cart_items': cart_items
    }
    return render(request, 'products/cart.html', context)

def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id = item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated.')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id = item_id)
    product_name = cart_item.product.product
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart.')
    return redirect('view_cart')
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> a412d636ba4b0367d9a976319838e4e6159e37af
