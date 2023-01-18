from django import forms
from .models import Comment
from django.core.validators import validate_image_file_extension

class CommentForm(forms.Form):
    content = forms.CharField()
    star = forms.IntegerField(max_value=5,min_value=0)
    thumbnail = forms.ImageField(
        widget=forms.FileInput,
        required=False,
        validators=[validate_image_file_extension],
    )

    def save(self, commit=True):
        self.instance = Comment(**self.cleaned_data)
        if commit:
            self.instance.save()
        return self.instance