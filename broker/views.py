from django.shortcuts import render, redirect
from property_manager.decorators import property_dealer_required, broker_required
from property_manager.models import PropertyDealer, Property, Image, Document
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BrokerForm, BrokerProfileUpdateForm
from property_manager.forms import CustomPasswordChangeForm
from tanant.models import Tanant
from django.db.models import Q
from .models import Broker, BrokerFile
from django.core.paginator import Paginator
User = get_user_model()


# ================ Tenant Dashboard Views Start =================

@login_required(login_url="signin")
@broker_required
def broker_dashboard(request):
    """
    Dashboard for Broker.
    """

    all_properties = Property.objects.filter(Q(property_type='free') | Q(property_type='off-plan')).count()
    all_tenants = Tanant.objects.filter(broker__user=request.user).count()
    free_properties = Property.objects.filter(property_type='free').count()
    off_plan_properties = Property.objects.filter(property_type='off-plan').count()
    context = {
        'all_tenants': all_tenants,
        "all_properties": all_properties,
        "free_properties": free_properties,
        "off_plan_properties": off_plan_properties
    }
    return render(request, "broker-dashboard.html", context)

# ================ Tenant Dashboard Views End =================


# ================ Property Manager Profile Views Start =================


@login_required(login_url="signin")
@broker_required
def broker_profile(request):
    """
    Broker Profile.
    """

    broker = Broker.objects.filter(user=request.user, user__is_broker=True).first()
    if request.method == "POST":
        form = BrokerProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            broker = Broker.objects.filter(user=user, user__is_broker=True).first()
            broker.company_name = form.cleaned_data["company_name"]
            broker.contact_number = form.cleaned_data["contact_number"]
            broker.address = form.cleaned_data["address"]
            broker.website = form.cleaned_data["city"]
            if 'logo' in form.cleaned_data and form.cleaned_data['logo'] is not None:
                broker.logo = form.cleaned_data["logo"]
            broker.save()
            messages.success(request, "Profile updated successfully")
            return redirect("broker-profile")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return redirect("broker-profile")
    context = {
        "broker": broker
    }
    return render(request, "broker-profile.html", context)

@login_required(login_url="signin")
@broker_required
def change_broker_password(request):
    """
    Process the password change for a user and provide feedback.
    """

    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password updated successfully")
            return redirect("broker-profile")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return redirect("broker-profile")
    return render(request, "broker-profile.html")


# ================ Broker Profile Views End =================


@login_required(login_url="signin")
@property_dealer_required
def broker_list(request):
    """
    Displays a list of brokers.
    """

    brokers = Broker.objects.filter(user__is_broker=True).order_by('-created_date')
    paginator = Paginator(brokers, 7)
    page_number = request.GET.get("page")
    brokers = paginator.get_page(page_number)
    context = {
        'brokers': brokers
    }
    return render(request, "broker/broker-list.html", context)


@login_required(login_url="signin")
@property_dealer_required
def create_broker(request):
    """
    Manages the process of adding the broker.
    """

    if request.method == "POST":
        form = BrokerForm(request.POST, request.FILES)
        if form.is_valid():
            broker_instance = form.save(commit=False)

            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            conform_password = form.cleaned_data["confirm_password"]
            user = User.objects.filter(username=username).exists()
            if user:
                messages.error(request, "User already exists with that username")
                return redirect("create-broker")
            if password != conform_password:
                messages.error(request, "Password do not match")
                return redirect("create-broker")
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_broker = True
            user.save()
            broker_instance.user = user
            broker_instance.save()

            # Handle Images
            profile_picture = request.FILES.get('logo')
            file_instance = BrokerFile(file=profile_picture, type='profile')
            file_instance.save()
            broker_instance.files.add(file_instance)

            # Handle Images
            images = request.FILES.getlist('images')
            for image in images:
                image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
                extension = image.name.lower().rsplit('.', 1)[-1] if '.' in image.name else ''
                if extension in image_extensions:
                    file_type = 'image'
                else:
                    file_type = 'document'
                image_instance = BrokerFile(file=image, type=file_type)
                image_instance.save()
                broker_instance.files.add(image_instance)
            messages.success(request, "New Broker added successfully")
            return redirect("broker-list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}, {error}")
                    return redirect("create-broker")
    return render(request, "broker/create-broker.html")


@login_required(login_url="signin")
@property_dealer_required
def delete_broker(request, pk):
    """
    Deletes a broker by ID.
    """

    try:
        broker = Broker.objects.get(id=pk)
    except:
        messages.error(request, "Broker ID does not exist")
        return redirect("broker-list")
    if request.method == "POST":
        broker.delete()
        messages.success(request, "Broker deleted successfully")
        return redirect("broker-list")

    context = {
        'broker': broker
    }
    return render(request, "broker/delete-broker.html", context)


@login_required(login_url="signin")
@property_dealer_required
def view_broker(request, pk):
    """
    Displays details of a specific broker.
    """

    try:
        broker = Broker.objects.get(id=pk)
    except:
        messages.error(request, "Broker ID does not exist")
        return redirect("broker-list")
    context = {
        'broker': broker
    }
    return render(request, "broker/view-broker.html", context)


@login_required(login_url="signin")
@property_dealer_required
def edit_broker(request, pk):
    """
    Edit details of a specific broker.
    """

    try:
        broker = Broker.objects.get(id=pk)
        broker_username = broker.user.username
    except:
        messages.error(request, "Broker ID does not exist")
        return redirect("broker-list")
    if request.method == "POST":
        form = BrokerForm(request.POST, request.FILES, instance=broker)
        if form.is_valid():
            instance = form.save(commit=False)

            remove_images = request.POST.getlist('remove_images')
            for file_id in remove_images:
                file = BrokerFile.objects.get(id=file_id)
                file.delete()

            remove_documents = request.POST.getlist('remove_documents')
            for file_id in remove_documents:
                file = BrokerFile.objects.get(id=file_id)
                file.delete()

            profile_picture = request.FILES.get('logo')
            file_instance = instance.files.filter(type='profile').exists()
            remove_file_instance = instance.files.filter(type='profile')
            if not file_instance:
                file_instance = BrokerFile(file=profile_picture, type='profile')
                file_instance.save()
                instance.files.add(file_instance)
            else:
                for file_instances in remove_file_instance:
                    instance.files.remove(file_instances)
                file_instance = BrokerFile(file=profile_picture, type='profile')
                file_instance.save()
                instance.files.add(file_instance)

            images = request.FILES.getlist('images')
            for image in images:
                image_extensions = ('jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp')
                extension = image.name.lower().rsplit('.', 1)[-1] if '.' in image.name else ''
                if extension in image_extensions:
                    file_type = 'image'
                else:
                    file_type = 'document'
                image_instance = BrokerFile(file=image, type=file_type)
                image_instance.save()
                instance.files.add(image_instance)

            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            user = User.objects.get(username=broker_username)
            user.username = username
            user.email = email
            user.save()
            instance.user = user
            instance.save()
            messages.success(request, "Broker Updated successfully")
            return redirect("broker-list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}, {error}")
    context = {
        'broker': broker,
    }
    return render(request, "broker/edit-broker.html", context)