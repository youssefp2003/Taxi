from django import forms
from .models import Taxi, Driver, Reservation,Booking ,Review,User,DriverProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from .models import User
from .models import Client
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
# forms.py
from django import forms
from .models import Driver

class UpdateAvailabilityForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['availability']  # Add other fields if necessary

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('driver', 'Driver'),
        ('administrateur', 'Administrateur'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = ['availability']



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user

class TaxiForm(forms.ModelForm):
    class Meta:
        model = Taxi
        fields = ['registration_number','brand', 'model']

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['phone_number', 'address']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['pickup_location', 'destination', 'pickup_time', 'contact_number']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['taxi', 'rating', 'comment']

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['phone_number', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des champs si nécessaire
        self.fields['phone_number'].label = 'Numéro de téléphone'
        self.fields['address'].label = 'Adresse'
        self.fields['address'].widget = forms.Textarea(attrs={'rows': 3})


class DriverSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.DRIVER
        if commit:
            user.save()
        return user       
    
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role') 
        user_id = forms.IntegerField(widget=forms.HiddenInput())  # Champ caché pour l'ID utilisateur
        username = forms.CharField(max_length=150)
        email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})  # Ajoutez des classes CSS si nécessaire
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

    def clean_user_id(self):
        user_id = self.cleaned_data['user_id']
        if not User.objects.filter(id=user_id).exists():
            raise forms.ValidationError("Utilisateur non trouvé.")
        return user_id
    

class CancelBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []  # Ajoutez les champs spécifiques nécessaires pour annuler une réservation, comme 'status'

class ModifyBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []  # Ajoutez les champs spécifiques nécessaires pour modifier une réservation

    def __init__(self, *args, **kwargs):
        super(ModifyBookingForm, self).__init__(*args, **kwargs)
        # Personnalisez les champs ou ajoutez des validations si nécessaire


from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class AssignDriverForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['driver']

    driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.Select,
        label="Sélectionner un conducteur",
        empty_label="Sélectionner un conducteur"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver'].queryset = Driver.objects.all()
        self.fields['driver'].label_from_instance = lambda obj: f"{obj.user.username} ({obj.license_number})"