from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Order, OrderItem, Product


def sales_view(request):
    """Show products saved in PostgreSQL and current cart."""
    # Only shows available products
    products = Product.objects.filter(stock__gt=0)
    cart = request.session.get("cart", {})

    cart_total = 0.0
    for item in cart.values():
        cart_total += float(item["price"]) * int(item["quantity"])

    context = {
        "products": products,
        "cart": cart,
        "cart_total": round(cart_total, 2),
    }
    return render(request, "sales/sales.html", context)


def add_to_cart(request, product_id):
    """Add one product from db to the cart in current session."""
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get("cart", {})
        str_id = str(product_id)

        if str_id in cart:
            cart[str_id]["quantity"] += 1
        else:
            cart[str_id] = {
                "id": product.id,
                "name": product.name,
                "price": str(product.price),
                "quantity": 1,
            }

        request.session["cart"] = cart
        request.session.modified = True

    return redirect("sales:sales_list")


def process_order(request):
    """Save order and its items in PostgreSQL and
    clear cart session."""
    if request.method == "POST":
        cart = request.session.get("cart", {})

        if not cart:
            return redirect("sales:sales_list")

        order_total = sum(
            float(item["price"]) * item["quantity"] for item in cart.values()
        )

        # Register order in database
        new_order = Order.objects.create(total=order_total)

        # Register each Order Item and update stock
        for item in cart.values():
            product = Product.objects.get(id=item["id"])
            OrderItem.objects.create(
                order=new_order,
                product=product,
                quantity=item["quantity"],
                unit_price=item["price"],
            )
            # Descontar stock
            if product.stock >= item["quantity"]:
                product.stock -= item["quantity"]
                product.save()

        # Clean last session
        request.session["cart"] = {}
        request.session.modified = True

        return HttpResponse(
            f"<h1>Order #{new_order.id} saved successfully!</h1>"
            f"<a href='/sales/'>Go back to the store</a> | "
            f"<a href='/admin/sales/order/{new_order.id}/change/'>"
            "Ver en Admin</a>"
        )

    return redirect("sales:sales_list")
