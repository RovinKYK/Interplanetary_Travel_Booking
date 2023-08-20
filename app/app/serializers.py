from rest_framework import serializers
from .models import User, PaymentMethod, SeatingArrangement, Booking
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'password_hash', 'email', 'full_name', 'profile_photo_link']

class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['payment_id', 'user_id', 'card_number', 'card_expiry']

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatingArrangement
        fields = ['arrangement_id', 'spaceship_id', 'seat_number', 'availability', 'booking_id']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'user_id', 'schedule_id', 'payment_id',
            'total_price', 'num_passengers', 'starting_planet_id',
            'destination_planet_id', 'departure_date', 'spaceship_id',
            'is_completed'
        ]

# class UserLoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'password_hash']
#     def validate(self, data):
#         username = data.get('username')
#         password = data.get('password_hash')

#         # Authenticate the user
#         user = authenticate(username=username, password=password)
#         if user:
#             data['user'] = user
#         else:
#             raise serializers.ValidationError('Invalid credentials')

#         return data
    




# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

#     @classmethod
#     def get_token(cls, user):
#         token = super(MyTokenObtainPairSerializer, cls).get_token(user)

#         # Add custom claims
#         token['username'] = user.username
#         return token

# Serializer to Register a User
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('user_id', 'username', 'password_hash', 'email', 'full_name', 'profile_photo_link')
#         extra_kwargs = {'password_hash': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create(validated_data['username'], validated_data['password_hash'])

#         user.set_password(validated_data['password_hash'])
#         user.save()

#         return user

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