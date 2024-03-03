from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm
from property_manager.models import PropertyDealer
from property_manager.decorators import property_dealer_required


def signin(request):
    """
    Authenticate a user and redirect or display error based on credentials.
    """

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(
                request, "Authentication successful. You are now logged in"
            )
            return redirect("property-manager-dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("signin")

    return render(request, "user/signin.html")


# @unauthenticated_user
def signup(request):
    """
    Used to handle the signup functionality for property managers who are not authenticated.
    """

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_property_dealer = True
            user.save()
            PropertyDealer.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name'],
                contact_number=form.cleaned_data['contact_number'],
                address=form.cleaned_data['address'],
                website=form.cleaned_data['website'])
            messages.success(request, "Registration successful!")
            return redirect("signin")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}, {error}")
                    return redirect("signup")

    return render(request, "user/signup.html")


@login_required(login_url="signin")
def signout(request):
    """
    Signs out the currently authenticated user.
    """

    logout(request)
    messages.success(request, "Logout successful!")
    return redirect("signin")
