from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('', login_required(views.contacts_home), name='contact_home'),
    path('contacts/', login_required(views.contact_list), name='contact_list'),
    path('contacts/add/', login_required(views.add_contact), name='add_contact'),
    path('contacts/<int:contact_id>/',
         login_required(views.contact_detail), name='contact_detail'),
    path('contacts/<int:contact_id>/edit/',
         login_required(views.edit_contact), name='edit_contact'),
    path('contacts/<int:contact_id>/delete/',
         login_required(views.delete_contact), name='delete_contact'),
    path('contacts/search/', login_required(views.contact_search),
         name='contact_search'),
    path('contacts/upcoming_birthdays/',
         login_required(views.upcoming_birthdays), name='upcoming_birthdays'),
]
