from functools import wraps
from django.shortcuts import redirect

def property_dealer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_property_dealer:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('signin')
    return wrapper

def tenant_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_tenant:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('signin')
    return wrapper


def tenant_or_property_dealer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_tenant or request.user.is_property_dealer):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('signin')
    return wrapper


def broker_or_property_dealer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_broker or request.user.is_property_dealer):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('signin')
    return wrapper


def broker_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_broker:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('signin')
    return wrapper
