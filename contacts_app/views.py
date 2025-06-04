from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from .forms import ContactForm
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import BirthdayFilterForm
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator


def contacts_home(request):
    """
    Main page for managing contacts.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The page for selecting actions with contacts.
    """
    return render(request, 'contacts_app/contact_home.html')


@login_required
def add_contact(request):
    """
    Creating a new contact.

    If the method is POST, creates a new contact based on the entered data.
    If the method is GET, returns a form for data entry.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The page with a form for adding a contact.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST, user=request.user)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('contact_list')
    else:
        form = ContactForm(user=request.user)

    return render(request, 'contacts_app/add_contact.html', {'form': form})


@login_required
def contact_detail(request, contact_id):
    """
    Displays the details of a specific contact.

    Args:
        request (HttpRequest): The request object.
        contact_id (int): The contact's identifier.

    Returns:
        HttpResponse: The page with the contact's details.
    """
    contact = get_object_or_404(
        Contact, id=contact_id, user=request.user)
    return render(request, 'contacts_app/contact_detail.html', {'contact': contact})


@login_required
def edit_contact(request, contact_id):
    """
    Editing an existing contact.

    Loads the contact by its identifier and allows modifying its data.

    Args:
        request (HttpRequest): The request object.
        contact_id (int): The contact's identifier.

    Returns:
        HttpResponse: The page with a form for editing the contact.
    """
    contact = get_object_or_404(
        Contact, id=contact_id, user=request.user)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact, user=request.user)

    return render(request, 'contacts_app/edit_contact.html', {
        'form': form,
        'contact': contact
    })


@login_required
def delete_contact(request, contact_id):
    """
    Deleting a contact.

    Loads the contact by its identifier and deletes it upon confirmation.

    Args:
        request (HttpRequest): The request object.
        contact_id (int): The contact's identifier.

    Returns:
        HttpResponse: The contact deletion confirmation page.
    """
    contact = get_object_or_404(
        Contact, id=contact_id, user=request.user)
    contact.delete()
    return redirect('contact_list')


@login_required
def contact_list(request):
    """
    Displays a list of all contacts with search functionality.
    """
    query = request.GET.get('search', '').strip()
    contacts = Contact.objects.filter(
        user=request.user)

    if query:
        contacts = contacts.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query)
        )

    paginator = Paginator(contacts, 3)
    page_number = request.GET.get('page')
    contacts_page = paginator.get_page(page_number)

    return render(request, 'contacts_app/contact_list.html', {'contacts': contacts_page})


@login_required
def contact_search(request):
    """
    Searches for contacts based on the provided query.

    Args:
        request (HttpRequest): The request object, possibly containing a 'query' GET parameter.

    Returns:
        HttpResponse: The page with search results for contacts, or an empty field if no query has been entered.
    """
    query = request.GET.get('query', '')
    if query:
        contacts = Contact.objects.filter(name__icontains=query)
    else:
        contacts = []

    return render(request, 'contacts_app/contact_search.html', {'contacts': contacts, 'query': query})


@login_required
def upcoming_birthdays(request):
    """
    Retrieves contacts with upcoming birthdays within a selected period.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The page with contacts who have upcoming birthdays.
    """
    today = timezone.localdate()
    period = request.GET.get('period', 1)

    try:
        period = int(period)
    except ValueError:
        period = 1

    end_date = today + relativedelta(months=period)

    all_birthdays = Contact.objects.filter(
        user=request.user)

    results = []
    for contact in all_birthdays:
        contact_birthday_current_year = contact.birthday.replace(
            year=today.year)

        if contact_birthday_current_year < today:
            contact_birthday_next_year = contact.birthday.replace(
                year=today.year + 1)
        else:
            contact_birthday_next_year = contact_birthday_current_year

        if today <= contact_birthday_current_year <= end_date or today <= contact_birthday_next_year <= end_date:

            nearest_birthday = contact_birthday_current_year if contact_birthday_current_year >= today else contact_birthday_next_year
            results.append((contact, nearest_birthday))

    results.sort(key=lambda x: x[1])

    sorted_contacts = [contact for contact, birthday in results]

    form = BirthdayFilterForm(initial={'period': period})

    return render(request, 'contacts_app/upcoming_birthdays.html', {
        'upcoming_birthdays': sorted_contacts,
        'form': form,
    })
