from django.shortcuts import render

# Create your views here.

try: 
    product= Products.objects.get(id=product_id)
except Products.DoesNotExist:
    messages.error(request,"Products not found")
    return redirect("products")


try:
    cart_item created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        )
    cart_item.quantity += 1
    cart_item.full_clean()
    cart_item.save()

except Exception as e:
        messages.error(request, "Error adding item to cart")
    return redirect("products")

return redirect("cart")