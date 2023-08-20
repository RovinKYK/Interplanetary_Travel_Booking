from rest_framework import serializers
from .models import User, PaymentMethods, SeatingArrangement, Bookings
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'password_hash', 'email', 'full_name', 'profile_photo_link']

class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethods
        fields = ['payment_id', 'user_id', 'card_number', 'card_expiry']

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatingArrangement
        fields = ['arrangement_id', 'spaceship_id', 'seat_number', 'availability', 'booking_id']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = [
            'booking_id', 'user_id', 'schedule_id', 'payment_id',
            'total_price', 'num_passengers', 'starting_planet_id',
            'destination_planet_id', 'departure_date', 'spaceship_id',
            'is_completed'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'password_hash', 'email', 'full_name', 'profile_photo_link']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance