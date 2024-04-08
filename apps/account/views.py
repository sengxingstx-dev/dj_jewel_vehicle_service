from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction

from apps.car_rental.models import Customer, RentalAgent, Rental
from .forms import RegistrationForm, EditAgentProfileForm, EditCustomerProfileForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser or user.is_staff:
                return redirect('dashboard')

            # Redirect to the next URL if it exists, otherwise redirect to a default URL
            next_url = request.GET.get('next')

            if next_url:
                return redirect(next_url)

            return redirect('home')  # Replace 'dashboard' with the URL name of your dashboard view
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'account/login.html')


@transaction.atomic
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email').lower()
            phone = form.cleaned_data.get('phone')

            user = form.save()

            customer = Customer.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
            )

            login(request, user)

            messages.success(request, 'Registration successful. You are now logged in.')

            if user.is_superuser or user.is_staff:
                return redirect('dashboard')

            return redirect('home')  # Replace 'dashboard' with the URL name of your dashboard view
    else:
        form = RegistrationForm()

    return render(request, 'account/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def admin_profile_view(request):
    try:
        user = request.user
        agent = RentalAgent.objects.get(user=user)

        if request.method == 'POST':
            agent_form = EditAgentProfileForm(request.POST, request.FILES, instance=agent)

            if agent_form.is_valid():
                agent_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('admin-profile')
        else:
            agent_form = EditAgentProfileForm(instance=agent)

    except RentalAgent.DoesNotExist:
        # Handle the case when the RentalAgent does not exist for the current user
        agent = None
        print('RentalAgent does not exist.')
    except Exception as e:
        print('Error:', str(e))

    context = {
        'user': user,
        'agent': agent,
    }
    return render(request, 'dashboard/html/pages-profile.html', context)


def user_profile_view(request):
    user = request.user
    customer = Customer.objects.filter(user=user).first()

    # Retrieve booking history for the current user's profile
    booking_history = Rental.objects.filter(customer=customer).order_by('-updated_at')

    context = {'user': user, 'customer': customer, 'booking_history': booking_history}
    return render(request, 'account/profile.html', context)


def edit_user_profile_view(request, pk):
    user = request.user
    customer = Customer.objects.get(id=pk)

    try:
        if request.method == 'POST':

            customer_form = EditCustomerProfileForm(request.POST, request.FILES, instance=customer)

            if customer_form.is_valid():
                customer_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('user-profile')
            else:
                print('Error: ', customer_form.errors)
        else:
            customer_form = EditCustomerProfileForm(instance=customer)

    except Customer.DoesNotExist:
        # Handle the case when the Customer does not exist for the current user
        customer = None
        print('Customer does not exist.')
    except Exception as e:
        print('Error:', str(e))

    context = {'user': user, 'customer': customer}
    return render(request, 'account/edit-profile.html', context)
