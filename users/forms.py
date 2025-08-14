from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required= True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        users = User.objects.all()
        super(UserRegistrationForm, self).clean()
        email = self.cleaned_data.get('email')
        for user in users:
            if user.email == email:
                self._errors['email'] = self.error_class(['Please user different email as there is already an account under this email.'])
        return self.cleaned_data
