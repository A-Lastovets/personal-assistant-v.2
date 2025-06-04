from .forms import RegisterForm, LoginForm, ProfileForm, UserUpdateForm


from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from personal_assistant.views import HomePageView
from django.core.files.storage import default_storage
print(default_storage.__class__)

def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='users:login')
        else:
            return render(request, 'users/signup.html', context={"form": form})

    return render(request, 'users/signup.html', context={"form": RegisterForm()})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to='home')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(to='home')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')

    return render(request, 'users/login.html', {"form": form})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='users:login')


@login_required
def profile(request):
    if not hasattr(request.user, "profile"):
        from users_app.models import Profile
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()

            # Поточний аватар (до змін)
            current_avatar = profile_form.instance.avatar

            # ⛔ не видаляти дефолтний
            def is_custom_avatar(avatar):
                return avatar and "default_avatar.png" not in avatar.name

            # Якщо натиснуто "Clear"
            if request.POST.get("avatar-clear"):
                if is_custom_avatar(current_avatar):
                    current_avatar.delete(save=False)
                profile_form.instance.avatar = None
                profile_form.instance.save()
            else:
                # Якщо завантажено новий аватар
                if 'avatar' in request.FILES:
                    new_avatar = request.FILES['avatar']
                    if is_custom_avatar(current_avatar):
                        current_avatar.delete(save=False)
                    profile = profile_form.save(commit=False)
                    profile.avatar = new_avatar
                    profile.save()

            messages.success(request, "Profile updated successfully.")
            return redirect(to='users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    subject_template_name = 'users/password_reset_subject.txt'
