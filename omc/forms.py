from django import forms
from .models import Comment
from django.core.validators import validate_image_file_extension

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content','star','thumbnail',)
        widgets = {
            'content' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    # 'placeholder': 'content'
                }
            ),
            'star' : forms.NumberInput(
                attrs={
                    'class' : 'form-control',
                    'max' : '5',
                    'min' : '0',
                }
            ),
            'thumbnail' : forms.ImageField(
                validators=[validate_image_file_extension],
            ),
        }