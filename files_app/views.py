import os
import boto3
import mimetypes
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.views.generic import ListView
from .models import File
from .forms import FileUploadForm
import requests
from botocore.exceptions import NoCredentialsError

class FileListView(ListView):
    model = File
    template_name = 'files_app/file_list.html'
    context_object_name = 'files'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            user=self.request.user).order_by('-uploaded_at')

        category = self.request.GET.get('category')

        if category == 'all' or not category:
            return queryset

        if category in dict(self.model.CATEGORY_CHOICES).keys():
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_number = self.request.GET.get('page', 1)
        paginator = Paginator(self.get_queryset(), self.paginate_by)

        page_obj = paginator.get_page(page_number)

        context['files'] = page_obj
        context['is_paginated'] = paginator.num_pages > 1
        context['selected_category'] = self.request.GET.get('category', 'all')

        return context


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user

            file_name = file_instance.file.name
            file_extension = os.path.splitext(file_name)[1].lower()

            if file_extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
                file_instance.category = 'image'
            elif file_extension in ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv']:
                file_instance.category = 'video'
            elif file_extension in ['.mp3', '.flac', '.wav']:
                file_instance.category = 'audio'
            elif file_extension in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.csv']:
                file_instance.category = 'document'
            else:
                file_instance.category = 'other'

            try:
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME,
                )

                bucket_name = settings.AWS_STORAGE_BUCKET_NAME
                s3_key = f'{file_instance.user.username}/{file_name}'

                s3_client.upload_fileobj(
                    file_instance.file,
                    bucket_name,
                    s3_key,
                    ExtraArgs={'ACL': 'public-read'}
                )

                file_instance.file = f'https://{bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{s3_key}'
                file_instance.original_extension = file_extension
                file_instance.name = file_name

                file_instance.save()
                return redirect('file_list.html')
            except NoCredentialsError:
                form.add_error(None, "AWS credentials not available")
                return render(request, 'files_app/upload.html', {'form': form})
            except Exception as e:
                form.add_error(None, f"Error uploading file: {str(e)}")
                return render(request, 'files_app/upload.html', {'form': form})
    else:
        form = FileUploadForm()

    return render(request, 'files_app/upload.html', {'form': form})


def download_file(request, file_id):
    file_instance = get_object_or_404(File, id=file_id)
    file_url = file_instance.file

    try:
        response = requests.get(file_url)
        response.raise_for_status()

        file_name = file_instance.name
        file_extension = file_instance.original_extension or ''
        
        content_type, _ = mimetypes.guess_type(file_name + file_extension)
        if content_type is None:
            content_type = 'application/octet-stream'

        download_response = HttpResponse(response.content)
        download_response['Content-Disposition'] = f'attachment; filename="{file_name}{file_extension}"'
        download_response['Content-Type'] = content_type

        return download_response

    except requests.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
        return HttpResponse(f"Error: Failed to upload file. Error code: {e.response.status_code}", status=500)
    except Exception as e:
        print(f"Error: {str(e)}")
        return HttpResponse(f"Error: {str(e)}", status=500)


def delete_file(request, file_id):
    file_instance = get_object_or_404(File, id=file_id)
    s3_key = f'{file_instance.user.username}/{file_instance.name}'

    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        s3_client.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=s3_key
        )

        file_instance.delete()
        return redirect('file_list.html')

    except Exception as e:
        return HttpResponse(f"Error deleting file: {str(e)}", status=500)
