from django.contrib import admin
from .models import Contact
from django.utils import timezone
from dateutil.relativedelta import relativedelta

class UpcomingBirthdaysFilter(admin.SimpleListFilter):
    title = 'Upcoming Birthdays'
    parameter_name = 'upcoming_birthdays'

    def lookups(self, request, model_admin):
        return (
            (1, 'Next Month'),
            (3, 'Next 3 Months'),
            (6, 'Next 6 Months'),
            (12, 'Next 12 Months'),
        )

    def queryset(self, request, queryset):
        period = self.value()
        if period is not None:
            today = timezone.localdate()
            end_date = today + relativedelta(months=int(period))

            results = []
            for contact in queryset:
                contact_birthday_current_year = contact.birthday.replace(year=today.year)

                if contact_birthday_current_year < today:
                    contact_birthday_next_year = contact.birthday.replace(year=today.year + 1)
                else:
                    contact_birthday_next_year = contact_birthday_current_year

                if today <= contact_birthday_current_year <= end_date or today <= contact_birthday_next_year <= end_date:
                    results.append(contact)

            return queryset.filter(id__in=[contact.id for contact in results])

        return queryset

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'email', 'birthday')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = (UpcomingBirthdaysFilter, 'birthday')
