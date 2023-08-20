from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    profile_photo_link = models.URLField(null=True, blank=True)
    # ... other fields and methods

class PaymentMethods(models.Model):
    payment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=255)
    card_expiry = models.CharField(max_length=10)
    # ... other fields and methods

class Planet(models.Model):
    planet_id = models.AutoField(primary_key=True)
    planet_name = models.CharField(max_length=255)
    planet_photo_link = models.URLField(null=True, blank=True)
    # ... other fields and methods

class Destinations(models.Model):
    destination_id = models.AutoField(primary_key=True)
    planet_id = models.ForeignKey(Planet, on_delete=models.CASCADE)
    destination_name = models.CharField(max_length=255)
    destination_photo_link = models.URLField(null=True, blank=True)
    # ... other fields and methods

class Spaceships(models.Model):
    spaceship_id = models.AutoField(primary_key=True)
    spaceship_name = models.CharField(max_length=255)
    spaceship_photo_link = models.URLField(null=True, blank=True)
    seating_capacity = models.PositiveIntegerField()
    # ... other fields and methods

class SeatingArrangement(models.Model):
    arrangement_id = models.AutoField(primary_key=True)
    spaceship_id = models.ForeignKey(Spaceships, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    availability = models.BooleanField(default=True)
    booking_id = models.ForeignKey('Bookings', on_delete=models.CASCADE)
    # ... other fields and methods

class FlightSchedules(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    flight_group_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    spaceship_id = models.ForeignKey(Spaceships, on_delete=models.CASCADE)
    departure_planet_id = models.ForeignKey(Planet, related_name='departures', on_delete=models.CASCADE)
    destination_id = models.ForeignKey(Destinations, related_name='arrivals', on_delete=models.CASCADE)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    flight_photo_link = models.URLField(null=True, blank=True)
    # ... other fields and methods

class Bookings(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule_id = models.ForeignKey(FlightSchedules, on_delete=models.CASCADE)
    payment_id = models.ForeignKey(PaymentMethods, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    num_passengers = models.PositiveIntegerField()
    starting_planet_id = models.ForeignKey(Planet, related_name='starting_planets', on_delete=models.CASCADE)
    destination_planet_id = models.ForeignKey(Planet, related_name='destination_planets', on_delete=models.CASCADE)
    departure_date = models.DateField()
    spaceship_id = models.ForeignKey(Spaceships, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    # ... other fields and methods

class BookingStoppings(models.Model):
    booking_stopping_id = models.AutoField(primary_key=True)
    booking_id = models.ForeignKey(Bookings, on_delete=models.CASCADE)
    stop_planet_id = models.ForeignKey(Planet, on_delete=models.CASCADE)
    stop_destination_id = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    # ... other fields and methods

class PassengerEmails(models.Model):
    email_id = models.AutoField(primary_key=True)
    booking_id = models.ForeignKey(Bookings, on_delete=models.CASCADE)
    passenger_email = models.EmailField()
    # ... other fields and methods