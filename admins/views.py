from django.shortcuts import render, redirect,get_object_or_404
from .forms import SignUpForm, LoginForm,VaccinationCenterForm
from .models import Signup
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from common.models import *
from django.db.models import Count
from users.models import *
from django.contrib import messages
def Register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            # Check if the username or email already exists
            if Signup.objects.filter(username=username).exists() or Signup.objects.filter(email=email).exists():
                form.add_error('username', "Username or email already exists")
            else:
                password_hashed = make_password(password)
                user = Signup(username=username, password=password_hashed, email=email)
                user.save()
                return redirect('Login')
        else:
            form.add_error(None, 'Form is invalid')
    else:
        form = SignUpForm()
    
    return render(request, 'register1.html', {'form': form})

def Login1(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user1 = Signup.objects.get(username=username)
                if check_password(password, user1.password):
                    # Create a custom user object or manually manage sessions
                    request.session['user_id'] = user1.id
                    return redirect('dashboard')  # Redirect to the dashboard or home page after login
                else:
                    form.add_error('password', 'Invalid password')
            except Signup.DoesNotExist:
                form.add_error('username', 'User does not exist')
    else:
        form = LoginForm()
    
    return render(request, 'login1.html', {'form': form})
def Dashboard(request):
    return render(request,'dashboard.html')

# Admin: Add Vaccination Center
def add_center(request):
    if request.method == 'POST':
        form = VaccinationCenterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('center_list')
    else:
        form = VaccinationCenterForm()
    return render(request, 'add_center.html', {'form': form})

def update_center(request, center_id):
    center = get_object_or_404(VaccinationCenter, id=center_id)
    if request.method == 'POST':
        form = VaccinationCenterForm(request.POST, instance=center)
        if form.is_valid():
            form.save()
            return redirect('center_list')  # Redirect to the center list after update
    else:
        form = VaccinationCenterForm(instance=center)
    
    return render(request, 'update_center.html', {'form': form, 'center': center})
# Admin: Delete Vaccination Center
def delete_center(request, center_id):
    center = VaccinationCenter.objects.get(id=center_id)
    center.delete()
    return redirect('center_list')

# Admin: List Vaccination Centers
def center_list(request):
    centers = VaccinationCenter.objects.all()
    return render(request, 'center_list.html', {'centers': centers})

def dosage_details(request):
    # Annotate each center with the total number of slots booked
    centers = VaccinationCenter.objects.all().annotate(
        total_doses=Count('slot_bookings')
    )

    return render(request, 'dosage_details.html', {'centers': centers})

def view_booked_slots(request):
    # if not request.user.is_staff:
    #     return redirect('login')  # Redirect non-admin users
    
    
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        status = request.POST.get('status')

        try:
            booking = SlotBooking.objects.get(id=booking_id)
            booking.status = status
            booking.save()
            messages.success(request, 'Booking status updated successfully!')
        except SlotBooking.DoesNotExist:
            messages.error(request, 'Booking does not exist.')

    bookings = SlotBooking.objects.select_related('center', 'user').all()
    return render(request, 'admin_booked_slots.html', {'bookings': bookings})
def logout1(request):
    return render(request,"logout1.html")
