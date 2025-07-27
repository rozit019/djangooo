from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task  # if you're using a Task model

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority']
 # or a specific list like ['title', 'description']


class RegisterForm(UserCreationForm):
    confpassword = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Django already handles password1 & password2

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        confpassword = cleaned_data.get("confpassword")

        if password1 and confpassword and password1 != confpassword:
            self.add_error("confpassword", "Passwords do not match")

#cd "/c/Users/rojit aryal/Desktop/jango"
#python -m venv ram
#source ram/Scripts/activate
#pip install django
#python manage.py runserver

