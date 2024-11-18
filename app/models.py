from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='media/destination_images/')

    # This will create an AutoField as the primary key
    # It will automatically assign unique IDs starting from 1
    id = models.AutoField(primary_key=True)


class Tour(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    guide = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    def price_in_cents(self):
        return int(self.price * 100)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    date_booked = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
from app.models import Destination



 


