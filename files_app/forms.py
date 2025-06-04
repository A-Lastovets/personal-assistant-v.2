from django import forms
from .models import File

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']

    def save(self, commit=True, user=None):
        file_instance = super().save(commit=False)
        file_instance.user = user

        if commit:
            file_instance.save()
        return file_instance
