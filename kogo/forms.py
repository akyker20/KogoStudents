from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
from registration.forms import RegistrationFormUniqueEmail
from django.core.exceptions import ValidationError

class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Duke netid'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))

    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form

class StudentRegistrationForm(RegistrationFormUniqueEmail):
    email = forms.RegexField(label="Duke Email", max_length=16,
        widget=forms.widgets.TextInput(attrs={'placeholder': 'netID@duke.edu'}),
        regex=r'^\D{3}\d{0,3}@duke\.edu$',
        error_messages={
            'invalid': "ex: amk46@duke.edu"})
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'more than 8 chars'}),
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'more than 8 chars'}),              
                                label="Password (again)")

    def __init__(self, *args, **kwargs): 
        super(StudentRegistrationForm, self).__init__(*args, **kwargs) 
        # remove username
        self.fields.pop('username')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError('Password too short')
        return password1