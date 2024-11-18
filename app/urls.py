from django.urls import path
from app import views
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import BookingConfirmationView


urlpatterns = [
    path('home', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/<int:pk>/', views.destination_detail, name='destination_detail'),
    path('tours/', views.tour_list, name='tour_list'),
    path('tours/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('destination/<int:pk>/book/', views.book_tour, name='book_tour'),
    path('account/', views.account, name='account'),
    path('account/edit/', views.edit_account, name='edit_account'),
    path('contact/', views.contact, name='contact'),
    path('', views.welcome, name='welcome'),
    path('about/', views.about, name='about'),
   
    path('booking-confirmation/<int:booking_id>/<int:pk>', BookingConfirmationView.as_view(), name='booking_confirmation'),
    path('paymentform/', views.payment_form, name='payment_form'),
    path('payment/<int:tour_id>/', views.payment, name='payment'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('daraja_payment_callback/', views.daraja_payment_callback, name='daraja_payment_callback'),
        
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




