from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        exclude = ['views', 'author']
        labels = {
            "title": "Nomi",
            "description": "Tavsifi",
            "genre": "Janri",
            "cover": "Poster",
            "video": "Video",
            "release": "Chiqqan sanasi",
        }
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Film nomini kiriting"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Film haqida qisqacha"
            }),
            "genre": forms.Select(attrs={
                "class": "form-select"
            }),
            "cover": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "video": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "release": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
        }
