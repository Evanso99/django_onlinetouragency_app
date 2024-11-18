

# Register your models here.

from django.contrib import admin
from .models import Destination, Tour, Booking

admin.site.register(Destination)
admin.site.register(Tour)
admin.site.register(Booking)
