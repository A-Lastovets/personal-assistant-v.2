from .forms import RegisterForm, LoginForm, ProfileForm, UserUpdateForm

import boto3
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.files.storage import default_storage

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


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
            profile = profile_form.instance
            current_avatar = profile.avatar

            def is_custom_avatar(avatar):
                return avatar and "default_avatar.png" not in avatar.name

            # Якщо завантажено новий файл — видаляємо попередній
            if 'avatar' in request.FILES:
                if is_custom_avatar(current_avatar):
                    default_storage.delete(current_avatar.name)
                profile.avatar = request.FILES['avatar']
                profile.save()
            else:
                profile_form.save()

            request.user.profile.refresh_from_db()
            messages.success(request, "Profile updated successfully.")
            return redirect(to='users:profile')
        else:
            messages.error(request, "Something went wrong. Please try again.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    avatar_path = request.user.profile.avatar.name if request.user.profile.avatar else None
    avatar_url = get_presigned_url(avatar_path) if avatar_path else None

    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'avatar_url': avatar_url
    })


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    subject_template_name = 'users/password_reset_subject.txt'


def get_presigned_url(path: str, expires_in: int = 3600) -> str:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": path},
        ExpiresIn=expires_in,
    )


@require_POST
@login_required
@csrf_exempt
def upload_avatar(request):
    avatar = request.FILES.get('avatar')
    if not avatar:
        return JsonResponse({'error': 'No file uploaded.'}, status=400)

    profile = request.user.profile

    if profile.avatar and "default_avatar.png" not in profile.avatar.name:
        profile.avatar.delete(save=False)

    profile.avatar = avatar
    profile.save()

    avatar_url = get_presigned_url(profile.avatar.name)
    return JsonResponse({'avatar_url': avatar_url})
