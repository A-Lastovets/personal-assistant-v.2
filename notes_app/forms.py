from django import forms
from .models import Note, Tag


class NoteForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Tags'
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']
        labels = {
            'title': 'Title',
            'content': 'Description',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NoteForm, self).__init__(*args, **kwargs)
        if user is not None:

            self.fields['tags'].queryset = Tag.objects.filter(created_by=user)
