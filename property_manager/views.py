from django.shortcuts import render, redirect
from .decorators import property_dealer_required
from .models import PropertyDealer, Property, Image, Document
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, CustomPasswordChangeForm, PropertyForm, TanantForm
from tanant.models import Tanant
from django.core.paginator import Paginator
User = get_user_model()


# ================ Property Manager Dashboard Views Start =================

@login_required(login_url="signin")
@property_dealer_required
def property_manager_dashboard(request):
    """
    Dashboard for Property Manager.
    """

    all_properties = Property.objects.filter(owner__user=request.user).count()
    sold_properties = Property.objects.filter(owner__user=request.user, status='sold').count()
    free_properties = Property.objects.filter(owner__user=request.user, status='free').count()
    rented_properties = Property.objects.filter(owner__user=request.user, status='rented').count()
    off_plan_properties = Property.objects.filter(owner__user=request.user, status='off-plan').count()
    all_tenants = Tanant.objects.all().count()
    context = {
        'all_properties': all_properties,
        'sold_properties': sold_properties,
        'free_properties': free_properties,
        'rented_properties': rented_properties,
        'off_plan_properties': off_plan_properties,
        'all_tenants': all_tenants
    }
    return render(request, "property-manager-dashboard.html", context)


# ================ Property Manager Dashboard Views End =================


# ================ Property Manager Profile Views Start =================


@login_required(login_url="signin")
@property_dealer_required
def property_manager_profile(request):
    """
    Property Manager Profile.
    """

    property_manager = PropertyDealer.objects.filter(user=request.user, user__is_property_dealer=True).first()
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            property_dealer = PropertyDealer.objects.filter(user=user).first()
            property_dealer.company_name = form.cleaned_data["company_name"]
            property_dealer.contact_number = form.cleaned_data["contact_number"]
            property_dealer.address = form.cleaned_data["address"]
            property_dealer.website = form.cleaned_data["website"]
            if 'logo' in form.cleaned_data and form.cleaned_data['logo'] is not None:
                property_dealer.logo = form.cleaned_data["logo"]
            property_dealer.save()
            messages.success(request, "Profile updated successfully")
            return redirect("property-manager-profile")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return redirect("property-manager-profile")
    context = {"property_manager": property_manager}
    return render(request, "property-manager-profile.html", context)

@login_required(login_url="signin")
@property_dealer_required
def change_password(request):
    """
    Process the password change for a user and provide feedback.
    """

    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password updated successfully")
            return redirect("property-manager-profile")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return redirect("property-manager-profile")
    return render(request, "property-manager-profile.html")


# ================ Property Manager Profile Views End =================


# ================ Property Views Start =================


@login_required(login_url="signin")
@property_dealer_required
def property_list(request):
    """
    Displays a list of properties.
    """

    properties = Property.objects.all()
    paginator = Paginator(properties, 7)
    page_number = request.GET.get("page")
    properties = paginator.get_page(page_number)
    context = {
        'properties': properties,
    }
    return render(request, "property/property-list.html", context)


@login_required(login_url="signin")
@property_dealer_required
def delete_property(request, pk):
    """
    Deletes a property by ID.
    """

    try:
        property = Property.objects.get(id=pk)
    except:
        messages.error(request, "Property ID does not exist")
        return redirect("property-list")
    if request.method == "POST":
        property.delete()
        messages.success(request, "Property deleted successfully")
        return redirect("property-list")

    context = {
        'property': property
    }
    return render(request, "property/delete-property.html", context)


@login_required(login_url="signin")
@property_dealer_required
def view_property(request, pk):
    """
    Displays details of a specific property.
    """

    try:
        property = Property.objects.get(id=pk)
    except:
        messages.error(request, "Property ID does not exist")
        return redirect("property-list")
    context = {
        'property': property
    }
    return render(request, "property/view-property.html", context)


@login_required(login_url="signin")
@property_dealer_required
def create_property(request):
    """
    Manages the process of adding the property.
    """

    if request.method == "POST":
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.owner = PropertyDealer.objects.get(user=request.user)
            property_instance.save()

            # Handle Images
            images = request.FILES.getlist('images')
            for image in images:
                image_instance = Image(image=image)
                image_instance.save()
                property_instance.images.add(image_instance)

            # Handle Documents
            documents = request.FILES.getlist('documents')
            for document in documents:
                document_instance = Document(file=document)
                document_instance.save()
                property_instance.documents.add(document_instance)

            messages.success(request, "New Property added successfully")
            return redirect("property-list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}, {error}")
                    return redirect("create-property")
    return render(request, "property/create-property.html")


@login_required(login_url="signin")
@property_dealer_required
def edit_property(request, pk):
    """
    Edit details of a specific property
    """

    try:
        property = Property.objects.get(id=pk)
    except:
        messages.error(request, "Property ID does not exist")
        return redirect("property-list")
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            instance = form.save(commit=False)

            remove_images = request.POST.getlist('remove_images')
            for image_id in remove_images:
                image = Image.objects.get(id=image_id)
                image.delete()

            remove_documents = request.POST.getlist('remove_documents')
            for document_id in remove_documents:
                document = Document.objects.get(id=document_id)
                document.delete()

            images = request.FILES.getlist('images')
            for image in images:
                image_instance = Image(image=image)
                image_instance.save()
                instance.images.add(image_instance)

            instance.save()
            messages.success(request, "Property Updated successfully")
            return redirect("property-list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}, {error}")


    context = {
        'property': property
    }
    return render(request, "property/edit-property.html", context)


# ================ Property Views Start =================


# ================ Tenant Views Start =================


@login_required(login_url="signin")
@property_dealer_required
def tenant_list(request):
    """
    Displays a list of tenants.
    """

    tenants = Tanant.objects.filter(user__is_tenant=True)
    paginator = Paginator(tenants, 7)
    page_number = request.GET.get("page")
    tenants = paginator.get_page(page_number)
    context = {
        'tenants': tenants
    }
    return render(request, "tenant/tenant-list.html", context)


@login_required(login_url="signin")
@property_dealer_required
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
            if password != conform_password:
                messages.error(request, "Password do not match")
                return redirect("create-tenant")
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_tenant = True
            user.save()
            tenant_instance.user = user

            # Handle Images
            file = request.FILES.get('agreement_document')
            file_instance = Document(file=file)
            file_instance.save()
            tenant_instance.agreement_document = file_instance
            tenant_instance.save()


            # Handle Images
            images = request.FILES.getlist('images')
            for image in images:
                image_instance = Image(image=image)
                image_instance.save()
                tenant_instance.images.add(image_instance)
            messages.success(request, "New Tenant added successfully")
            return redirect("tenant-list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}, {error}")
                    return redirect("create-tenant")
    properties = Property.objects.filter(owner__user=request.user)
    context = {
        'properties': properties
    }
    return render(request, "tenant/create-tenant.html", context)


@login_required(login_url="signin")
@property_dealer_required
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

    context = {
        'tenant': tenant
    }
    return render(request, "tenant/delete-tenant.html", context)


@login_required(login_url="signin")
@property_dealer_required
def view_tenant(request, pk):
    """
    Displays details of a specific tenant.
    """

    try:
        tenant = Tanant.objects.get(id=pk)
    except:
        messages.error(request, "Tenant ID does not exist")
        return redirect("tenant-list")
    context = {
        'tenant': tenant
    }
    return render(request, "tenant/view-tenant.html", context)


@login_required(login_url="signin")
@property_dealer_required
def edit_tenant(request, pk):
    """
    Edit details of a specific tenant.
    """

    try:
        tenant = Tanant.objects.get(id=pk)
        tenant_document_agreement = tenant.agreement_document
        tenant_username = tenant.user.username
        properties = Property.objects.filter(owner__user=request.user, owner__user__is_property_dealer=True)
    except:
        messages.error(request, "Tenant ID does not exist")
        return redirect("tenant-list")
    if request.method == "POST":
        form = TanantForm(request.POST, request.FILES, instance=tenant)
        if form.is_valid():
            instance = form.save(commit=False)

            remove_images = request.POST.getlist('remove_images')
            for image_id in remove_images:
                image = Image.objects.get(id=image_id)
                image.delete()

            file = request.FILES.get('agreement_document')
            if 'agreement_document' in request.FILES:
                file_instance = Document(file=file)
                file_instance.save()
                instance.agreement_document = file_instance
            else:
                instance.agreement_document = tenant_document_agreement

            images = request.FILES.getlist('images')
            for image in images:
                image_instance = Image(image=image)
                image_instance.save()
                instance.images.add(image_instance)

            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            user = User.objects.get(username=tenant_username)
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
    context = {
        'tenant': tenant,
        'properties': properties
    }
    return render(request, "tenant/edit-tenant.html", context)