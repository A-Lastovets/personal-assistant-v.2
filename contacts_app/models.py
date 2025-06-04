from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.conf import settings


class Contact(models.Model):
    """
    Model for storing contact information in a contact book.

    Attributes:
        user (User): The user who owns the contact.
        name (str): The contact's name.
        address (str): The contact's address.
        phone_number (PhoneNumberField): The contact's phone number.
        email (str): The contact's email.
        birthday (date): The contact's birthday.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone_number = PhoneNumberField(null=False, blank=False)
    email = models.EmailField()
    birthday = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'phone_number'], name='unique_user_phone_number'),
            models.UniqueConstraint(fields=['user', 'email'], name='unique_user_email'),
        ]

    def __str__(self):
        return self.name

    def days_until_birthday(self):
        """
        Calculates the number of days until the next birthday.

        Returns:
            int: The number of days until the next birthday, or None if the birthday is not specified.
        """
        if not self.birthday:
            return None

        today = timezone.now().date()
        next_birthday = self.birthday.replace(year=today.year)

        if next_birthday < today:
            next_birthday = self.birthday.replace(year=today.year + 1)

        return (next_birthday - today).days
