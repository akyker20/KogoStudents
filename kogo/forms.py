from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate

class NewStudentForm(UserCreationForm):

    #Make this a regex field eventually
    username = forms.CharField(label="Duke netid", max_length=8)
    
    class Meta:
        model = User
        fields = ( "username", "first_name", "last_name" )

    def save(self, commit=True):
        user = super(NewStudentForm, self).save(commit=False)
        user.email = "{}@duke.edu".format(self.cleaned_data["username"])
        if commit:
            user.save()
        return user



class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Duke netid'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))

    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form