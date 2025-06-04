from django.contrib import admin
from .models import Tag, Note
from .forms import NoteForm

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    form = NoteForm
    list_display = ('title', 'content', 'created_at')
    search_fields = ('title', 'content')
