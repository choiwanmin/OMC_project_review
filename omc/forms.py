from django import forms
from .models import Comment, User
from django.core.validators import validate_image_file_extension
from django.contrib.auth.forms import UserCreationForm

class CommentForm(forms.Form):

    content = forms.CharField(max_length=100,
        # label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': '댓글을 입력해주세요.',
            'rows': 4,
            'cols': 80
        })
    )
    # star = forms.IntegerField(max_value=5,min_value=0)
    star = forms.IntegerField(required=True,
        # label='',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '별점을 부여해주세요.',
            'style':'width:22ch'
        })
    )
    thumbnail = forms.ImageField(widget=forms.FileInput,
        required=False,
        validators=[validate_image_file_extension],
        # label=''
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
