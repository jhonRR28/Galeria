# gallery/forms.py
from django import forms
from .models import Image, Gallery

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'description', 'image_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la imagen'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la imagen', 'rows': 3}),
            'image_file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title', 'description', 'photo']