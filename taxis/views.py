from django.shortcuts import render, get_object_or_404, redirect
from .models import Taxi, Booking, Review,Driver, DriverProfile,Report,Client
from .forms import TaxiForm, BookingForm, ReviewForm, DriverForm, UserForm,UserRegistrationForm,ClientForm,AvailabilityForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, logout
from taxis.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .forms import UpdateAvailabilityForm,CustomUserChangeForm,DriverSignUpForm,DriverForm,CustomUserCreationForm

def index(request):
    user = request.user
    is_client = user.groups.filter(name='Client').exists()
    taxis = Taxi.objects.all()  # Exemple de récupération des taxis, adaptez selon vos besoins

    context = {
        'is_client': is_client,
        'taxis': taxis,
    }
    return render(request, 'taxis/index.html', context)

#walo-----------------------------------------------------------------------------------------------------------
def list_drivers(request):
    drivers = User.objects.filter(role=User.DRIVER)
    context = {
        'drivers': drivers,
    }
    return render(request, 'taxis/administrateur/list_drivers.html', context)
def view_reports(request):
    reports = Report.objects.all()  # Récupérer tous les rapports (exemple)
    context = {
        'reports': reports
    }
    return render(request, 'taxis/administrateur/view_reports.html', context)
def driver_signup(request):
    if request.method == 'POST':
        form = DriverSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige vers la page de connexion après inscription
    else:
        form = DriverSignUpForm()
    return render(request, 'taxis/driver/driver_signup.html', {'form': form})
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            # Sauvegarder le formulaire si valide
            client = form.save(commit=False)
            client.user = request.user  # Associer le client à l'utilisateur connecté
            client.save()
            return redirect('client_dashboard')  # Rediriger vers le tableau de bord client ou une autre vue
    else:
        form = ClientForm()
    
    return render(request, 'taxis/add_client.html', {'form': form})
def taxi_detail(request, taxi_id):
    taxi = get_object_or_404(Taxi, pk=taxi_id)
    return render(request, 'taxis/taxi_detail.html', {'taxi': taxi})
def manage_users(request):
    users = User.objects.all()
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')  # Redirige vers la page de gestion des utilisateurs après ajout

    context = {
        'users': users,
        'form': form,
    }
    return render(request, 'taxis/administrateur/manage_users.html', context)

#client--------------------------------------------------------------------------------------------------------------------
@login_required
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Réservation créée avec succès.')
            return redirect('user_bookings')
        else:
            messages.error(request, 'Erreur lors de la création de la réservation.')
    else:
        form = BookingForm()
    return render(request, 'taxis/client/create_booking.html', {'form': form})

@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    if not bookings:
        messages.info(request, 'Aucune réservation trouvée.')
    return render(request, 'taxis/client/user_bookings.html', {'bookings': bookings})

@login_required
def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('list_reviews')
    else:
        form = ReviewForm()
    return render(request, 'taxis/client/submit_review.html', {'form': form})

def list_reviews(request):
    reviews = Review.objects.all()
    return render(request, 'taxis/client/list_reviews.html', {'reviews': reviews})

@login_required
def cancel_reservation(request, reservation_id):
    booking = get_object_or_404(Booking, id=reservation_id, user=request.user)
    booking.delete()
    return redirect('user_bookings')

#driver--------------------------------------------------------------------------------------------------------------------
@login_required
def contact_client(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    client = booking.client.user  # Accéder à l'objet User du client

    # Implémentez votre logique de contact ici, comme l'envoi d'un email ou d'un message

    context = {
        'booking': booking,
        'client': client,
    }
    return render(request, 'taxis/driver/contact_client.html', context)

@login_required
def view_assignments(request):
    try:
        # Fetch the driver instance related to the logged-in user
        driver = Driver.objects.get(user=request.user)
        # Filter bookings assigned to this driver
        bookings = Booking.objects.filter(driver=driver)
        return render(request, 'taxis/driver/view_assignments.html', {'bookings': bookings})
    except Driver.DoesNotExist:
        # User is not a driver
        return render(request, 'taxis/error.html', {'message': "Vous n'êtes pas autorisé à voir cette page."})
    
@login_required
def update_availability(request):
    # Ensure a Driver instance exists for the logged-in user
    driver, created = Driver.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UpdateAvailabilityForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('driver_dashboard')
    else:
        form = UpdateAvailabilityForm(instance=driver)

    return render(request, 'taxis/driver/update_availability.html', {'form': form})

@login_required
def driver_profile(request):
    if request.user.groups.filter(name='Driver').exists():
        driver_profile = DriverProfile.objects.get(user=request.user)
        return render(request, 'taxis/driver/driver_profile.html', {'driver_profile': driver_profile})
    else:
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour accéder à cette page.")
        return redirect('index')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Booking, Message
from .forms import MessageForm

@login_required
def send_message(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = booking.user
            message.booking = booking
            message.save()
            return redirect('view_assignments')
    else:
        form = MessageForm()
    return render(request, 'taxis/driver/send_message.html', {'form': form, 'booking': booking})

#ADMIN--------------------------------------------------------------------------------------------------------------------
@login_required
def add_taxi(request):
    if request.method == "POST":
        form = TaxiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_taxis')
    else:
        form = TaxiForm()
    return render(request, 'taxis/administrateur/add_taxi.html', {'form': form})

def list_taxis(request):
    taxis = Taxi.objects.filter(available=True)  # Assurez-vous que vous utilisez 'available' correctement ici
    return render(request, 'taxis/administrateur/list_taxis.html', {'taxis': taxis})

@login_required
def add_driver(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        driver_form = DriverForm(request.POST)
        if user_form.is_valid() and driver_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'driver'  # Assignez le rôle de conducteur
            user.save()
            driver = driver_form.save(commit=False)
            driver.user = user
            driver.save()
            return redirect('list_drivers')  # Redirige vers la liste des conducteurs
    else:
        user_form = UserForm()
        driver_form = DriverForm()
    return render(request, 'taxis/administrateur/add_driver.html', {'user_form': user_form, 'driver_form': driver_form})
 #no
def manage_drivers(request):
    drivers = Driver.objects.all()
    form = DriverForm()

    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_drivers')

    context = {
        'drivers': drivers,
        'form': form,
    }
    return render(request, 'taxis/administrateur/manage_drivers.html', context)

@login_required
def delete_driver(request, driver_id):
    driver = get_object_or_404(User, id=driver_id, role=User.DRIVER)  # Récupère le conducteur par son ID et son rôle
    if request.method == 'POST':
        driver.delete()
        return redirect('list_drivers')
    context = {
        'driver': driver,
    }
    return render(request, 'taxis/administrateur/delete_driver.html', context)

@login_required
def edit_driver(request, driver_id):
    driver = get_object_or_404(User, id=driver_id)
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('list_drivers')  # Redirection vers la liste des conducteurs après modification
    else:
        form = DriverForm(instance=driver)
    
    context = {
        'form': form,
        'driver': driver,
    }
    return render(request, 'taxis/administrateur/edit_driver.html', context)

def manage_clients(request):
    clients = User.objects.filter(role=User.CLIENT)  # Filtrer par le rôle CLIENT

    context = {
        'clients': clients,
    }
    return render(request, 'taxis/administrateur/manage_clients.html', context)

def delete_client(request, client_id):
    client = get_object_or_404(User, pk=client_id)
    
    if request.method == 'POST':
        client.delete()
        return redirect('manage_clients')

    context = {
        'client': client,
    }
    return render(request, 'taxis/administrateur/delete_client.html', context)

def edit_client(request, client_id):
    client = get_object_or_404(User, id=client_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('manage_clients')  # Redirection après modification
    else:
        form = CustomUserChangeForm(instance=client)
    
    context = {
        'form': form,
        'client': client,
    }
    return render(request, 'taxis/administrateur/edit_client.html', context)

def manage_taxis(request):
    taxis = Taxi.objects.all()  # Récupérer tous les taxis (exemple)
    context = {
        'taxis': taxis
    }
    return render(request, 'taxis/administrateur/manage_taxis.html', context)

from .forms import AssignDriverForm

@login_required
def assign_driver(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        form = AssignDriverForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirigez vers la page des assignations
    else:
        form = AssignDriverForm(instance=booking)
    return render(request, 'taxis/administrateur/assign_driver.html', {'form': form, 'booking': booking})


@login_required
def unassigned_bookings(request):
    bookings = Booking.objects.filter(driver__isnull=True)
    return render(request, 'taxis/administrateur/unassigned_bookings.html', {'bookings': bookings})


def edit_taxi(request, taxi_id):
    taxi = get_object_or_404(Taxi, pk=taxi_id)
    if request.method == 'POST':
        form = TaxiForm(request.POST, instance=taxi)
        if form.is_valid():
            form.save()
            return redirect('manage_taxis')  # Rediriger vers la gestion des taxis après modification
    else:
        form = TaxiForm(instance=taxi)
    
    context = {
        'form': form,
        'taxi': taxi
    }
    return render(request, 'taxis/administrateur/edit_taxi.html', context)

def delete_taxi(request, taxi_id):
    taxi = get_object_or_404(Taxi, pk=taxi_id)
    if request.method == 'POST':
        taxi.delete()
        return redirect('manage_taxis')  # Rediriger vers la gestion des taxis après suppression
    
    context = {
        'taxi': taxi
    }
    return render(request, 'taxis/administrateur/delete_taxi.html', context)

def manage_bookings(request):
    bookings = Booking.objects.all()
    context = {
        'bookings': bookings
    }
    return render(request, 'taxis/administrateur/manage_bookings.html', context)

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    
    if request.method == 'POST':
        booking.delete()
        # Redirect to a success page or another appropriate URL after deletion
        return redirect('booking_list')  # Redirect to booking list page or home page
    
    # If the request method is not POST (e.g., GET), render a confirmation template
    return render(request, 'taxis/administrateur/cancel_booking.html', {'booking': booking})

def modify_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            # Redirect to a success page or the updated booking details page
            return redirect('booking_detail', booking_id=booking_id)
    else:
        form = BookingForm(instance=booking)
    
    return render(request, 'taxis/administrateur/modify_booking.html', {'form': form})

#connexion
def is_driver(user):
    return user.role == 'driver'

def is_administrateur(user):
    return user.role == 'administrateur'

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data['role']  # Assurez-vous que votre formulaire capture correctement le rôle
            user.role = role
            user.save()
            if role == 'driver':
                Driver.objects.create(user=user)
            elif role == 'client':
                Client.objects.create(user=user)
            # Other actions after saving the user
            login(request, user)
            # Autres actions après l'enregistrement
            return redirect('index')  # Redirige vers la page d'accueil après inscription
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'taxis/registration/signup.html', {'form': form})

@login_required
def home(request):
    if request.user.role == 'client':
        return redirect('client_dashboard')
    elif request.user.role == 'driver':
        return redirect('driver_dashboard')
    elif request.user.role == 'administrateur':
        return redirect('administrateur_dashboard')
    else:
        return redirect('index')

def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('index')
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user role
                if hasattr(user, 'driver'):
                    return redirect('driver_dashboard')
                elif hasattr(user, 'administrateur'):
                    return redirect('admin_dashboard')
                elif hasattr(user, 'client'):
                    return redirect('client_dashboard')
                else:
                    return render(request, 'error.html', {'message': "L'utilisateur n'est pas associé à un conducteur."})
    else:
        form = AuthenticationForm()
    return render(request, 'taxis/registration/login.html', {'form': form})

@login_required
def role_based_redirect(request):
    user = request.user
    if user.role == 'client':
        return redirect('client_dashboard')
    elif user.role == 'driver':
        return redirect('driver_dashboard')
    elif user.role == 'administrateur':
        return redirect('administrateur_dashboard')
    else:
        return redirect('login')  # or handle unknown role

@login_required
def client_dashboard(request):
    return render(request, 'taxis/dashboard/client_dashboard.html')

@login_required
@user_passes_test(is_driver)
def driver_dashboard(request):
    return render(request, 'taxis/dashboard/driver_dashboard.html')

@login_required
@user_passes_test(is_administrateur)
def administrateur_dashboard(request):
    return render(request, 'taxis/dashboard/administrateur_dashboard.html')
