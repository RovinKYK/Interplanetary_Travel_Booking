from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(PaymentMethod)
admin.site.register(Booking)
admin.site.register(SeatingArrangement)
