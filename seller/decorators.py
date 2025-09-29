from django.shortcuts import redirect
from functools import wraps


def approved_seller_required(view_func):
    from seller.views import get_seller
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        seller = get_seller(request)   
        if not seller.is_approved:
            return redirect("sellerdashboard")   
        return view_func(request, *args, **kwargs)
    return wrapper




