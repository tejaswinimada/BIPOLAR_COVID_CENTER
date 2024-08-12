from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import*
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.decorators import login_required
from .forms import *
from common.models import *
from django.db.models import Count
from django.contrib.auth import login as auth_login,authenticate
def home(request):
    return render(request,'home.html')

def Registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            address = form.cleaned_data.get('address')
            phonenumber = form.cleaned_data.get('phonenumber')
            
            # Create UserProfile object
            UserProfile.objects.create(
                user=user,
                address=address,
                phonenumber=phonenumber
            )
            auth_login(request, user)
            messages.success(request, 'Registration successful')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Login successful')
            return redirect('dashboard1')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def dashboard1(request):
    return render(request, "dashboard1.html") 

@login_required
def search_centers(request):
    centers = VaccinationCenter.objects.all()
    query = request.GET.get('q')
    if query:
        centers = centers.filter(name__icontains=query)
    return render(request, 'search_centers.html', {'centers': centers})


#   Ensure the user is logged in
@login_required
def book_slot(request, center_id):
    center = get_object_or_404(VaccinationCenter, id=center_id)
    
    if request.method == 'POST':
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')

        # Check if the slot is available
        existing_bookings = SlotBooking.objects.filter(center=center, date=date, time_slot=time_slot).count()
        if existing_bookings >= 10:
            messages.error(request, 'This slot is fully booked. Please choose another slot.')
        else:
            # Fetch the custom user instance
            try:
                user = UserProfile.objects.get(pk=request.user.id)
            except UserProfile.DoesNotExist:
                messages.error(request, 'User does not exist.')
                return redirect('Login')  # Redirect to login or handle appropriately

            # Create a new booking
            SlotBooking.objects.create(
                user=user,
                center=center,
                date=date,
                time_slot=time_slot
            )
            messages.success(request, 'Slot booked successfully!')
            return redirect('search_centers')

    return render(request, 'book_slot.html', {'center': center})
def logout(request):
    return render(request,'logout.html')
