from django.urls import path, reverse
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from .views import logout_view

class CustomLoginView(auth_views.LoginView):
    def get_success_url(self):
        return reverse('role_based_redirect')

urlpatterns = [
    path('', views.index, name='index'),
    #walo
    path('client/taxi_details/<int:taxi_id>/', views.taxi_detail, name='taxi_detail'), 
    path('view_reports/', views.view_reports, name='view_reports'),
    path('manage_users/', views.manage_users, name='manage_users'),

    #client
    path('create-booking/', views.create_booking, name='create_booking'),
    path('user-bookings/', views.user_bookings, name='user_bookings'),
    path('submit-review/', views.submit_review, name='submit_review'),
    path('list-reviews/', views.list_reviews, name='list_reviews'),
    path('client/cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
   
    #driver
    path('driver/assignments/', views.view_assignments, name='view_assignments'),
    path('driver/update_availability/', views.update_availability, name='update_availability'),
    path('driver/profile/', views.driver_profile, name='driver_profile'),
    path('contact-client/<int:booking_id>/', views.contact_client, name='contact_client'),
    path('signup-driver/', views.driver_signup, name='driver_signup'),
    path('driver/send_message/<int:booking_id>/', views.send_message, name='send_message'),

    #admin
    path('list-drivers/', views.list_drivers, name='list_drivers'),
    path('add-driver/', views.add_driver, name='add_driver'),
    path('manage_drivers/', views.manage_drivers, name='manage_drivers'), 
    path('edit_driver/<int:driver_id>/', views.edit_driver, name='edit_driver'),
    path('delete_driver/<int:driver_id>/', views.delete_driver, name='delete_driver'),

    path('manage_clients/', views.manage_clients, name='manage_clients'), 
    path('delete_client/<int:client_id>/', views.delete_client, name='delete_client'),
    path('edit-client/<int:client_id>/', views.edit_client, name='edit_client'),

    path('add_taxi/', views.add_taxi, name='add_taxi'),
    path('manage_taxis/', views.manage_taxis, name='manage_taxis'),
    path('edit_taxi/<int:taxi_id>/', views.edit_taxi, name='edit_taxi'),
    path('delete_taxi/<int:taxi_id>/', views.delete_taxi, name='delete_taxi'),
    path('list-taxis/', views.list_taxis, name='list_taxis'),
   
    path('manage-bookings/', views.manage_bookings, name='manage_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('modify-booking/<int:booking_id>/', views.modify_booking, name='modify_booking'),
    path('administrateur/assign_driver/<int:booking_id>/', views.assign_driver, name='assign_driver'),
    path('administrateur/unassigned_bookings/', views.unassigned_bookings, name='unassigned_bookings'),
    #connexion
    path('login/', auth_views.LoginView.as_view(template_name='taxis/registration/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='taxis/registration/login.html')),
    path('role_based_redirect/', views.role_based_redirect, name='role_based_redirect'),
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('driver/dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('administrateur/dashboard/', views.administrateur_dashboard, name='administrateur_dashboard'),
]