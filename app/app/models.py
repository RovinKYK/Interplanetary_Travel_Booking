from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    profile_photo_link = models.URLField(null=True, blank=True)
    # ... other fields and methods

class PaymentMethod(models.Model):
    payment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=255)
    card_expiry = models.CharField(max_length=10)

class Planet(models.Model):
    planet_id = models.AutoField(primary_key=True)
    planet_name = models.CharField(max_length=255)
    #planet_photo_link = models.URLField(null=True, blank=True)
    # ... other fields and methods

class Destinations(models.Model):
    destination_id = models.AutoField(primary_key=True)
    planet_id = models.ForeignKey(Planet, on_delete=models.CASCADE)
    destination_name = models.CharField(max_length=255)
    #destination_photo_link = models.URLField(null=True, blank=True)
    # ... other fields and methods

class Spaceships(models.Model):
    spaceship_id = models.AutoField(primary_key=True)
    spaceship_name = models.CharField(max_length=255)
    #spaceship_photo_link = models.URLField(null=True, blank=True)
    seating_capacity = models.PositiveIntegerField()
    company = models.CharField(max_length=255)
    # ... other fields and methods

class FlightSchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    spaceship_id = models.ForeignKey(Spaceships, on_delete=models.CASCADE)
    departure_planet_id = models.ForeignKey(Planet, related_name='departures', on_delete=models.CASCADE)
    destination_id = models.ForeignKey(Destinations, related_name='arrivals', on_delete=models.CASCADE)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    #flight_photo_link = models.URLField(null=True, blank=True)
    prices = models.DecimalField(max_digits=10, decimal_places=2)
    # ... other fields and methods

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule_id = models.ForeignKey(FlightSchedule, on_delete=models.CASCADE)
    num_passengers = models.PositiveIntegerField()
    starting_planet = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_date = models.DateField()
    spaceship_name = models.CharField(max_length=255)
    spaceship_company = models.CharField(max_length=255)
    # ... other fields and methods


class Seat(models.Model):
    seat_id = models.AutoField(primary_key=True)
    spaceship_id = models.ForeignKey(Spaceships, on_delete=models.CASCADE)
    availability = models.BooleanField(default=True)
    booking_id = models.ForeignKey(Booking, blank=True, null=True, on_delete=models.DO_NOTHING)
    # ... other fields and methods


class Bookingtoppings(models.Model):
    booking_stopping_id = models.AutoField(primary_key=True)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    stop_planet_id = models.ForeignKey(Planet, on_delete=models.CASCADE)
    stop_destination_id = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    # ... other fields and methods

class PassengerEmails(models.Model):
    email_id = models.AutoField(primary_key=True)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    passenger_email = models.EmailField()
    # ... other fields and methods