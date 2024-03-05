from django.shortcuts import render, redirect
from property_manager.decorators import property_dealer_required, broker_or_property_dealer_required
from property_manager.models import PropertyDealer, Property, Image, Document
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TanantForm
from .models import Tanant, TanantFile
from broker.models import Broker
from django.core.paginator import Paginator
from django.core.files.images import get_image_dimensions
User = get_user_model()

# Create your views here.


@login_required(login_url="signin")
@broker_or_property_dealer_required
def tenant_list(request):
    """
    Displays a list of tenants.
    """

    if request.user.is_broker:
        tenants = Tanant.objects.filter(broker__user=request.user,user__is_tenant=True).order_by('-created_date')
    if request.user.is_property_dealer:
        tenants = Tanant.objects.filter(user__is_tenant=True).order_by('-created_date')
    paginator = Paginator(tenants, 7)
    page_number = request.GET.get("page")
    tenants = paginator.get_page(page_number)
    if request.user.is_broker:
        base_template = 'broker-base.html'
    else:
        base_template = 'base.html'
    context = {
        'base_template': base_template,
        'tenants': tenants
    }
    return render(request, "tenant/tenant-list.html", context)


@login_required(login_url="signin")
@property_dealer_required
def broker_tenant_list(request):
    """
    Displays a list of tenants.
    """

    tenants = Tanant.objects.filter(user__is_tenant=True, broker__isnull=False).order_by('-created_date')
    paginator = Paginator(tenants, 7)
    page_number = request.GET.get("page")
    tenants = paginator.get_page(page_number)
    context = {
        'tenants': tenants
    }
    return render(request, "tenant/broker-tenant-list.html", context)


@login_required(login_url="signin")
@broker_or_property_dealer_required
def create_tenant(request):
    """
    Manages the process of adding the tenant.
    """

    if request.method == "POST":
        form = TanantForm(request.POST, request.FILES)
        if form.is_valid():
            tenant_instance = form.save(commit=False)

            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            conform_password = form.cleaned_data["confirm_password"]
            user = User.objects.filter(username=username).exists()
            if user:
                messages.error(request, "User already exists with that username")
                return redirect("create-tenant")
            if password != conform_password:
                messages.error(request, "Password do not match")
                return redirect("create-tenant")
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_tenant = True
            if request.user.is_broker:
                broker = Broker.objects.get(user=request.user)
                tenant_instance.broker = broker
            user.save()
            tenant_instance.user = user
            tenant_instance.save()

            # Handle Images
            profile_picture = request.FILES.get('logo')
            file_instance = TanantFile(file=profile_picture, type='profile')
            file_instance.save()
            tenant_instance.files.add(file_instance)


            # Handle Images
            images = request.FILES.getlist('images')
            for image in images:
                try:
                    get_image_dimensions(image)
                    file_type = 'image'
                except:
                    file_type = 'document'
                image_instance = TanantFile(file=image, type=file_type)
                image_instance.save()
                tenant_instance.files.add(image_instance)
            messages.success(request, "New Tenant added successfully")
            return redirect("tenant-list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}, {error}")
                    return redirect("create-tenant")
    properties = Property.objects.all()
    if request.user.is_broker:
        base_template = 'broker-base.html'
    else:
        base_template = 'base.html'
    context = {
        'properties': properties,
        'base_template': base_template
    }
    return render(request, "tenant/create-tenant.html", context)


@login_required(login_url="signin")
@broker_or_property_dealer_required
def delete_tenant(request, pk):
    """
    Deletes a tenant by ID.
    """

    try:
        tenant = Tanant.objects.get(id=pk)
    except:
        messages.error(request, "Tenant ID does not exist")
        return redirect("tenant-list")
    if request.method == "POST":
        tenant.delete()
        messages.success(request, "Tenant deleted successfully")
        return redirect("tenant-list")
    if request.user.is_broker:
        base_template = 'broker-base.html'
    else:
        base_template = 'base.html'

    context = {
        'base_template': base_template,
        'tenant': tenant
    }
    return render(request, "tenant/delete-tenant.html", context)


@login_required(login_url="signin")
@broker_or_property_dealer_required
def view_tenant(request, pk):
    """
    Displays details of a specific tenant.
    """

    try:
        tenant = Tanant.objects.get(id=pk)
    except:
        messages.error(request, "Tenant ID does not exist")
        return redirect("tenant-list")
    if request.user.is_broker:
        base_template = 'broker-base.html'
    else:
        base_template = 'base.html'
    context = {
        'tenant': tenant,
        'base_template': base_template
    }
    return render(request, "tenant/view-tenant.html", context)


@login_required(login_url="signin")
@broker_or_property_dealer_required
def edit_tenant(request, pk):
    """
    Edit details of a specific tenant.
    """

    try:
        tenant = Tanant.objects.get(id=pk)
        tenant_username = tenant.user.username
        properties = Property.objects.filter(owner__user__is_property_dealer=True)
    except:
        messages.error(request, "Tenant ID does not exist")
        return redirect("tenant-list")
    if request.method == "POST":
        form = TanantForm(request.POST, request.FILES, instance=tenant)
        if form.is_valid():
            instance = form.save(commit=False)

            remove_images = request.POST.getlist('remove_images')
            for file_id in remove_images:
                file = TanantFile.objects.get(id=file_id)
                file.delete()

            remove_documents = request.POST.getlist('remove_documents')
            for file_id in remove_documents:
                file = TanantFile.objects.get(id=file_id)
                file.delete()

            file = request.FILES.get('logo')
            if 'logo' in request.FILES:
                file_instance = TanantFile(file=file, type='profile')
                file_instance.save()
                instance.files.add(file_instance)

            images = request.FILES.getlist('images')
            for image in images:
                image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
                extension = image.name.lower().rsplit('.', 1)[-1] if '.' in image.name else ''
                if extension in image_extensions:
                    file_type = 'image'
                else:
                    file_type = 'document'
                image_instance = TanantFile(file=image, type=file_type)
                image_instance.save()
                instance.files.add(image_instance)


            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            user = User.objects.get(username=tenant_username)

            if request.user.is_broker:
                broker = Broker.objects.get(user=request.user)
                instance.broker = broker

            user.username = username
            user.email = email
            user.save()
            instance.user = user
            instance.save()
            messages.success(request, "Tenant Updated successfully")
            return redirect("tenant-list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}, {error}")

    if request.user.is_broker:
        base_template = 'broker-base.html'
    else:
        base_template = 'base.html'

    context = {
        'tenant': tenant,
        'properties': properties,
        'base_template': base_template
    }
    return render(request, "tenant/edit-tenant.html", context)