import datetime
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

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