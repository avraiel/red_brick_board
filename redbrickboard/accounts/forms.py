from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

from django import forms

from django.forms.widgets import PasswordInput, EmailInput

# Authenticate a User // Login
class CustomUserAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=PasswordInput())
    def __init__(self, *args, **kwargs): 
        super(CustomUserAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True 
        self.fields.pop('username')
        self.order_fields(['email', 'password'])
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

# Registering a User Form
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2", "first_name", "last_name", "role", "picture", "bio"]
    
    # Labelling password2 as "Confirm Password"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].label = 'Confirm Password'

    # This method runs automatically when forms are submitted, the email is an ateneo email address
    def clean_email(self):
        data = self.cleaned_data['email']
        if "@ateneo.edu" not in data and "@student.ateneo.edu" not in data and "@alumni.ateneo.edu" not in data:   
            raise forms.ValidationError("Must be an ateneo email address")
        return data


# class CustomUserCreationForm(forms.ModelForm):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
#     password = forms.CharField(widget=PasswordInput())

# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = CustomUser
#         fields = ("username", "email")