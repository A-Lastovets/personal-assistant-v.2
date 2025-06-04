from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        })
    )

    password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )

    password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        })
    )

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        labels = {
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(
            *args, **kwargs)
        for field, label in self.Meta.labels.items():
            self.fields[field].label = label

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.email.lower()
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Email"
        self.fields["password"].label = "Password"

    def clean_email(self):
        return self.cleaned_data['email'].lower()


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    gender = forms.ChoiceField(
        required=False,
        choices=Profile.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'avatar', 'phone', 'address', 'gender']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'avatar': 'Avatar',
            'phone': 'Phone',
            'address': 'Address',
            'gender': 'Gender',
        }

    def save(self, commit=True):
        profile = super().save(commit=False)

        if profile.first_name:
            profile.first_name = profile.first_name.strip().capitalize()

        if profile.last_name:
            profile.last_name = profile.last_name.strip().capitalize()

        if profile.phone:
            profile.phone = profile.phone.strip()

        if profile.address:
            profile.address = profile.address.strip().title()

        if commit:
            profile.save()
        return profile


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.email.lower()
        if commit:
            user.save()
        return user
