from django.db import models
from django.conf import settings
import os

class File(models.Model):
    CATEGORY_CHOICES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    
    file = models.FileField(
        upload_to='uploads/%Y/%m/%d/%u/',
        blank=False,
        null=False
    )
    
    original_extension = models.CharField(max_length=10, blank=True, null=True)
    
    public_id = models.CharField(max_length=255, blank=True, null=True)
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    resource_type = models.CharField(max_length=50, null=True, blank=True)

    preview = models.FileField(upload_to='previews/', blank=True, null=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        file_name = self.file.name.lower()
        file_extension = os.path.splitext(file_name)[1]

        if file_extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
            self.category = 'image'
        elif file_extension in ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv']:
            self.category = 'video'
        elif file_extension in ['.mp3', '.flac', '.wav']:
            self.category = 'audio'
        elif file_extension in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.csv']:
            self.category = 'document'
        else:
            self.category = 'other'

        self.original_extension = file_extension
        super().save(*args, **kwargs)
