from django.contrib import admin
from .models import Driver, Taxi, Reservation ,Booking, Review, User,Report
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_number', 'phone_number')
    search_fields = ('name', 'license_number')

@admin.register(Taxi)
class TaxiAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'brand', 'model', 'driver')
    search_fields = ('registration_number', 'brand', 'model')
    list_filter = ('brand',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('taxi', 'passenger_name', 'pickup_location', 'dropoff_location', 'pickup_time', 'dropoff_time')
    search_fields = ('passenger_name', 'pickup_location', 'dropoff_location')
    list_filter = ('pickup_time', 'dropoff_time')

admin.site.register(Booking)
admin.site.register(Review)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email', 'role')


admin.site.register(Report)
