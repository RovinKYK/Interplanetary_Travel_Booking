import datetime
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed
import jwt, json
from django.contrib.auth.hashers import check_password
from django.db.models import Q


def index(request):
    return HttpResponse("Hello, world.")

@api_view(['GET','POST'])
def payment_method_list(request, format=None):
    if request.method == 'GET':
        paymentMethods = PaymentMethod.objects.all()
        serializer = PaySerializer(paymentMethods, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = PaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET','PUT', 'DELETE'])
def payment_method_details(request, payment_id, format=None):

    try:
        paymentMethod = PaymentMethod.objects.get(pk=payment_id)
    except PaymentMethod.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':        
        serializer = PaySerializer(paymentMethod)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PaySerializer(paymentMethod, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         
    elif request.method == 'DELETE':
        paymentMethod.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def completed_bookings_list(request, id, format=None):
    if request.method == 'GET':
        bookings = Booking.objects.select_related('schedule_id').filter(user_id=id, schedule_id__arrival_datetime__lte=datetime.datetime.now())
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
        
@api_view(['GET'])
def pending_bookings_list(request, id, format=None):
    if request.method == 'GET':
        bookings = Booking.objects.select_related('schedule_id').filter(user_id=id, schedule_id__arrival_datetime__gte=datetime.datetime.now())
        serializer1 = BookingSerializer(bookings, many=True)
        return Response(serializer1.data)
    
    if request.method == 'POST':
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED) 

@api_view(['GET','POST'])
def available_seat_list(request, flight_id, format=None):
    if request.method == 'GET':
        availablesSeats = Seat.objects.filter(spaceship_id=flight_id)
        serializer = SeatSerializer(availablesSeats, many=True)
        return Response(serializer.data)   
    
@api_view(['GET','PUT', 'DELETE'])
def seat_arrangement_details(request, arrangement_id, format=None):
    try:
        seat = Seat.objects.get(pk=arrangement_id)
    except Seat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':        
        serializer = SeatSerializer(seat)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = SeatSerializer(seat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         
    elif request.method == 'DELETE':
        seat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to register
def register_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([])
def login_view(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password_hash']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        # if not user.check_password(password):
        if  password != user.password_hash:
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

@api_view(['GET'])
def user_view(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user = User.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def logout_view(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'success'
    }
    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def available_flights_view(request):
    data = json.loads(request.body)
    # Get query parameters from the request
    departure_planet_id = data.get('departure_planet_id')
    destination_id = data.get('destination_id')
    selected_date = data.get('selected_date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    print(data)

    # Combine date and time strings into datetime objects
    # Convert the selected date and times to datetime objects
    selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
    start_time = datetime.datetime.strptime(start_time, '%H:%M:%S').time()
    end_time = datetime.datetime.strptime(end_time, '%H:%M:%S').time()

    # Combine the selected date and start time to create the start datetime
    start_datetime = datetime.datetime.combine(selected_date.date(), start_time)

    # Combine the selected date and end time to create the end datetime
    end_datetime = datetime.datetime.combine(selected_date.date(), end_time)

    # Query for flight schedules that match the criteria
    matching_flights = FlightSchedule.objects.filter(
        departure_planet_id=departure_planet_id,
        destination_id=destination_id,
        departure_datetime__date=selected_date
    ).exclude(
        Q(departure_datetime__lt=start_datetime) | Q(arrival_datetime__gt=end_datetime)
    )

    # Serialize the flight schedules and return the response
    serializer = FlightSchedulesSerializer(matching_flights, many=True)
    return Response(serializer.data)
