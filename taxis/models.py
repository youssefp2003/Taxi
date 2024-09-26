from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser,AbstractBaseUser


class User(AbstractUser):
    CLIENT = 'client'
    DRIVER = 'driver'
    ADMINISTRATEUR = 'administrateur'

    ROLE_CHOICES = [
        (CLIENT, 'Client'),
        (DRIVER, 'Driver'),
        (ADMINISTRATEUR, 'Administrateur'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    def role_css_class(self):
        if self.role == self.CLIENT:
            return 'client'
        elif self.role == self.DRIVER:
            return 'driver'
        elif self.role == self.ADMINISTRATEUR:
            return 'administrateur'
        return ''
    # Ajoutez vos champs personnalisés si nécessaire
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='taxis_users'  # related_name distinct pour groups
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='taxis_users'  # related_name distinct pour user_permissions
    )
    def __str__(self):
        return self.username
    
class Driver(models.Model):
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, default='Unknown')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    availability = models.BooleanField(default=True)
    def __str__(self):
        return self.user.username
    def __str__(self):
        return self.name
    def __str__(self):
        return self.user.get_full_name() 

class Taxi(models.Model):
    registration_number = models.CharField(max_length=50)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    available = models.BooleanField(default=True)  # Assurez-vous que ce champ est défini correctement

    def __str__(self):
        return self.registration_number
    
#imkn supp reservation
class Reservation(models.Model):
    taxi = models.ForeignKey(Taxi, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=100)
    pickup_location = models.CharField(max_length=200)
    dropoff_location = models.CharField(max_length=200)
    pickup_time = models.DateTimeField()
    dropoff_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.passenger_name} - {self.taxi}"
    def cancel(self):
        self.status = 'cancelled'
        self.save()



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    #taxi = models.ForeignKey(Taxi, on_delete=models.CASCADE,default=1)
    pickup_location = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    pickup_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    def __str__(self):
        return f"Booking for {self.user.username} at {self.pickup_time}"
    def cancel(self):
        self.status = 'cancelled'
        self.save()



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    taxi = models.ForeignKey(Taxi, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.taxi.registration_number} - {self.rating}'
    


class Assignment(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    details = models.TextField()

    def __str__(self):
        return f"{self.driver.username} - {self.date}"

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    availability = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
    
class Report(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # Autres champs spécifiques aux rapports

    def __str__(self):
        return self.title
    
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.user.username
    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} for Booking {self.booking.id}"
