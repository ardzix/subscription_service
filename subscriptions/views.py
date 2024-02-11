from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import SignUpForm, TenantForm, SubscriptionForm
from .models import Tenant, Package, Subscription


def home(request):
    # Fetch all packages, assuming you want to display all of them on the home page
    packages = Package.objects.prefetch_related('benefits').all()
    tenant_count = Tenant.objects.filter(owned_by=request.user).count() if not request.user.is_anonymous else 0

    # Pass the packages to the template
    context = {'packages': packages, 'tenant_count': tenant_count}
    return render(request, 'subscriptions/home.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until it is confirmed
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('subscriptions/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'subscriptions/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'subscriptions/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Corrected line
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # Ensure you have a URL named 'home' in your URLconf
        return redirect('home')
    else:
        return render(request, 'subscriptions/account_activation_invalid.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page.
            # Adjust the redirect as needed
            return redirect('manage_subscriptions')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  # Adjust the redirect as needed
    else:
        return render(request, 'subscriptions/login.html')


def logout_view(request):
    logout(request)
    # Instead of redirecting, render the 'logged_out.html' template
    return render(request, 'subscriptions/logged_out.html')


@login_required
def manage_tenants(request):
    tenants = Tenant.objects.filter(owned_by=request.user)
    return render(request, 'subscriptions/manage_tenants.html', {'tenants': tenants})


@login_required
def manage_subscriptions(request):
    subscriptions = Subscription.objects.filter(tenant__owned_by=request.user)
    packages = Package.objects.all()  # Add logic as needed to filter or order packages
    return render(request, 'subscriptions/manage_subscriptions.html', {'subscriptions': subscriptions, 'packages': packages})


@login_required
def add_tenant(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            tenant = form.save(commit=False)
            tenant.owned_by = request.user  # Set the tenant's owner to the current user
            tenant.save()
            # Default to manage tenants if no next parameter
            next_url = request.GET.get('next', reverse('manage_tenants'))
            return redirect(next_url)
    else:
        form = TenantForm()
    return render(request, 'subscriptions/add_tenant.html', {'form': form})


@login_required
def edit_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id, owned_by=request.user)
    try:
        subscription = Subscription.objects.get(tenant=tenant)
    except Subscription.DoesNotExist:
        subscription = None  # No subscription exists for this tenant

    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            # Redirect to tenant management page or wherever appropriate
            return redirect('manage_tenants')
    else:
        form = TenantForm(instance=tenant)

    # Pass both form and subscription (if any) to the template
    return render(request, 'subscriptions/edit_tenant.html', {'form': form, 'tenant': tenant, 'subscription': subscription})


@login_required
def subscribe(request):
    # Extract package_id from query parameters
    package_id = request.GET.get('package_id')
    initial_data = {}

    if not Tenant.objects.filter(owned_by=request.user).exists():
        # Build the return URL
        # 'subscribe' is the name of your subscribe view
        next_url = reverse('subscribe')
        package_id = request.GET.get('package_id')
        if package_id:
            next_url += f"?package_id={package_id}"
        # 'add_tenant' is the name of your add tenant view
        return_url = f"{reverse('add_tenant')}?next={next_url}"
        return redirect(return_url)

    if package_id:
        # Ensure the package exists and is accessible to the user
        package = get_object_or_404(Package, id=package_id)
        initial_data['package'] = package

    if request.method == 'POST':
        form = SubscriptionForm(request.POST, user=request.user)
        if form.is_valid():
            subscription = form.save(commit=False)

            # Calculate end_date based on duration choice
            start_date = timezone.now().date()  # Assuming subscription starts now
            if form.cleaned_data['duration'] == 'monthly':
                end_date = start_date + timedelta(days=30)
            else:  # 'annually'
                end_date = start_date + timedelta(days=365)

            subscription.start_date = start_date
            subscription.end_date = end_date

            subscription.save()

            # Redirect to a confirmation page or payment page as needed
            return redirect('subscription_success')
    else:
        form = SubscriptionForm(user=request.user, initial=initial_data)

    return render(request, 'subscriptions/subscribe.html', {'form': form})


@login_required
def subscription_success(request):
    # Render a simple success message template
    return render(request, 'subscriptions/subscription_success.html')
