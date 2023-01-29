from django import forms
from .models import Comment, User
from django.core.validators import validate_image_file_extension
from django.contrib.auth.forms import UserCreationForm

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

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields= ("email", "nickname", "password1", "password2", "gender", "ageGroup", "householdSize")
