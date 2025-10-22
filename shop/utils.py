from .models import Cart, CartItem

def get_user_cart(request):
    """Return or create cart for logged-in user"""
    if not request.user.is_authenticated:
        return None
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return cart


def get_guest_cart(request):
    """Return or create cart for guest (using session_id)"""
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    cart, _ = Cart.objects.get_or_create(session_id=session_id, user=None)
    return cart


def merge_guest_cart_to_user(request):
    """Merge guest cart into user cart after login"""
    if not request.user.is_authenticated:
        return

    guest_cart = get_guest_cart(request)
    if not guest_cart.items.exists():
        return  # no guest cart to merge

    user_cart = get_user_cart(request)

    # Merge items
    for item in guest_cart.items.all():
        existing = user_cart.items.filter(product=item.product).first()
        if existing:
            existing.quantity += item.quantity
            existing.save()
        else:
            item.cart = user_cart
            item.save()

    # Delete guest cart after merge
    guest_cart.delete()
