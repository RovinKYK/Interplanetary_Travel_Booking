from rest_framework import serializers
from .models import *

class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethods
        fields = ['payment_id', 'card_number', 'card_expiry']
