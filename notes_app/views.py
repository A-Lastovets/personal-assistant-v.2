from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Note, Tag
from .forms import NoteForm


@login_required
def note_home(request):
    notes = Note.objects.filter(created_by=request.user)
    return render(request, 'notes_app/note_home.html', {'notes': notes})


@login_required
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.created_by = request.user
            note.save()

            tag_ids = request.POST.getlist('tags')
            for tag_id in tag_ids:
                if tag_id:
                    try:
                        tag = Tag.objects.get(
                            id=tag_id, created_by=request.user)
                        note.tags.add(tag)
                    except Tag.DoesNotExist:
                        continue

            new_tag_name = request.POST.get('new_tag')
            if new_tag_name:
                tag, created = Tag.objects.get_or_create(
                    name=new_tag_name.strip(),
                    defaults={'created_by': request.user}
                )
                if created:
                    note.tags.add(tag)

            return redirect('note_list')
    else:
        form = NoteForm()

    user_tags = Tag.objects.filter(created_by=request.user)
    return render(request, 'notes_app/add_note.html', {'form': form, 'tags': user_tags})


@login_required
def note_list(request):
    query = request.GET.get('q')
    tag_query = request.GET.get('tag')
    notes = Note.objects.filter(created_by=request.user).order_by('-created_at')

    if query:
        notes = notes.filter(
            Q(title__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()

    if tag_query:
        notes = notes.filter(tags__name__icontains=tag_query).distinct()

    paginator = Paginator(notes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'notes_app/note_list.html', {'page_obj': page_obj, 'query': query, 'tag_query': tag_query})


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, created_by=request.user)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.created_by = request.user
            note.save()

            note.tags.clear()
            tag_ids = request.POST.getlist('tags')
            for tag_id in tag_ids:
                if tag_id:
                    try:
                        tag = Tag.objects.get(
                            id=tag_id, created_by=request.user)
                        note.tags.add(tag)
                    except Tag.DoesNotExist:
                        continue

            new_tag_name = request.POST.get('new_tag')
            if new_tag_name:
                tag, created = Tag.objects.get_or_create(
                    name=new_tag_name.strip(),
                    defaults={'created_by': request.user}
                )
                if created:
                    note.tags.add(tag)

            return redirect('note_list')
    else:
        form = NoteForm(instance=note)

    user_tags = Tag.objects.filter(created_by=request.user)

    return render(request, 'notes_app/edit_note.html', {'form': form, 'note': note, 'tags': user_tags})


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, created_by=request.user)
    note.delete()
    return redirect('note_list')


@login_required
def note_list_sorted(request):
    tag = request.GET.get('tag')
    if tag:
        notes = Note.objects.filter(
            tags__name__icontains=tag, created_by=request.user)
    else:
        notes = Note.objects.filter(created_by=request.user)
    return render(request, 'notes_app/note_list.html', {'notes': notes})


@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id, created_by=request.user)
    return render(request, 'notes_app/note_detail.html', {'note': note})


@login_required
def add_tag(request):
    if request.method == "POST":
        tag_name = request.POST.get('name')
        if tag_name:
            tag, created = Tag.objects.get_or_create(
                name=tag_name.strip(),
                defaults={'created_by': request.user}
            )
            if created:
                messages.success(request, 'Tag added successfully!')
            else:
                messages.warning(request, 'Tag already exists!')
    return redirect(request.META.get('HTTP_REFERER', 'add_note'))
