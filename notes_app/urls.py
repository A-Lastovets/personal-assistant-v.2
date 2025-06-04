from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_home, name='note_home'),
    path('notes/add/', views.add_note, name='add_note'),
    path('notes/', views.note_list, name='note_list'),
    path('notes/edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('notes/delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('notes/<int:note_id>/', views.note_detail, name='note_detail'),
    path('add_tag/', views.add_tag, name='add_tag'),
]
