from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from .models import Destination
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from .models import Destination, Tour, Booking, User
from django.contrib.auth.decorators import login_required
from .models import Destination, Tour, Booking
from .forms import BookingForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from paypalrestsdk import Payment, exceptions
import paypalrestsdk
from .models import Booking
from django.http import HttpResponse
from .forms import BookingForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient


def home(request):
    destinations = Destination.objects.all()
    context = {'destinations': destinations}
    return render(request, 'base.html', context)

def welcome(request):
    return render(request, 'welcome.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid login details. Please try again.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logout(request):
    
     return render(request, 'logout.html')

def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = 'Password Reset Request'
            message = 'Please click the link below to reset your password:\n\n'
            message += f'{request.build_absolute_uri("/")[:-1]}{request.path}?token={email}'
            from_email = 'noreply@example.com'
            send_mail(subject, message, from_email, [email], fail_silently=False)
            messages.success(request, 'An email has been sent with instructions to reset your password.')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'forgot_password.html', {'form': form})

def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'destination_list.html', {'destinations': destinations})

def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    tour = destination.tour_set.first()  # first Tour object associated with this destination
    return render(request, 'destination_detail.html', {'destination': destination, 'tour': tour})

def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'tour_list.html', {'tours': tours})

def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    return render(request, 'tour_detail.html', {'tour': tour})

def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'booking_list.html', {'bookings': bookings})

def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'booking_detail.html', {'booking': booking})

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user_detail.html', {'user': user})

def home(request):
    return render(request, 'home.html')


@login_required
def book_tour(request, pk):
    destination = get_object_or_404(Destination, pk=pk )
    tour = get_object_or_404(Tour, destination=destination)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.tour = tour
            booking.save()
            return render(request, 'booking_confirmation.html', {'booking': booking})
    else:
        form = BookingForm()
    return render(request, 'book_tour.html', {'destination': destination, 'form': form, 'tour': tour})

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm


@login_required
def account(request):
    return render(request, 'account.html', {'user': request.user})

@login_required
def edit_account(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account details have been updated.')
            return redirect('account')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'edit_account.html', {'form': form})

@login_required
def account(request):
    return render(request, 'account.html', {'user': request.user})


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        # Send email
        send_mail(
            f'New message from {name} ({email})',
            message,
            email,
            ['evansofficial054@gmail.com'],  # Replace with your actual email address
            fail_silently=False,
        )

        return render(request, 'contact.html', {'success': True})

    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Tour, Booking
from .forms import BookingForm


def payment(request, tour_id):
    # Get the tour object
    tour = get_object_or_404(Tour, id=tour_id)

    # Get the total amount
    total = tour.price
    amount = int(total)  # Convert the total to an integer

    mpesa_client = MpesaClient()

    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            # Retrieve the phone number from the form
            phone_number = booking_form.cleaned_data['phone_number']

            # Prepare STK push details
            account_reference = 'reference'
            transaction_desc = 'Payment for your tour booking'
            callback_url = 'http://example.com/daraja-payment-callback'

            # Initiate STK Push
            response = mpesa_client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

            # Store relevant information in the session
            request.session['tour_id'] = tour.id

            return HttpResponse(response)
        else:
            # Handle invalid form input
            return HttpResponse("Invalid form data. Please check your inputs and try again.")
    else:
        # Render the form for the GET request
        booking_form = BookingForm()
        return render(request, 'payment_form.html', {'form': booking_form, 'tour': tour})






from .models import Destination, Tour, Booking

from django.shortcuts import redirect
from .models import Tour, Booking

def daraja_payment_callback(request):
    # Retrieve the tour ID from the session
    tour_id = request.session.get('tour_id')

    # Verify the M-Pesa callback here, ensure it's a valid transaction
    # You will need to implement this verification logic

    # If the M-Pesa payment is successful, create a booking
    if payment_successful:  # Implement your payment verification logic here
        tour = Tour.objects.get(id=tour_id)
        booking = Booking.objects.create(
            user=request.user,
            tour=tour,
            name=request.user.get_full_name(),
            email=request.user.email,
            phone_number=request.user.booking.phone_number
        )

        # Mark the tour as booked and save the booking
        tour.booked = True
        tour.save()
        booking.save()

        # Redirect the user to a confirmation page
        return redirect('confirmation')
    else:
        # Handle payment execution failure
        return HttpResponse('Error executing M-Pesa payment')



@method_decorator(login_required, name='dispatch')
class BookingConfirmationView(View):
    def get(self, request, booking_id):
        booking = Booking.objects.get(id=booking_id)
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')
        payment = Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            booking.paid = True
            booking.save()
            return render(request, 'booking_confirmation.html', {'booking': booking})
        else:
            return render(request, 'payment.html', {'booking': booking, 'error': 'Payment execution failed'})


def payment_form(request):
    return render(request, 'payment_form.html')

def confirmation(request):
    return render(request, 'confirmation.html')

