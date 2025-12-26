from django import forms
from django.contrib.admin.widgets import AdminDateWidget
#from users.models import UserProfile
from .models import Subscriber
from dal import autocomplete
from allauth.account.forms import LoginForm, ResetPasswordForm


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={"placeholder": "Введите ваш email", "autocomplete": "email", "class": "newsletter_input"})
        }


class UnsubscriberForm(forms.Form):
    email = forms.EmailField(
        label="Ваш email",
        widget=forms.EmailInput(attrs={
            "placeholder": "Введите ваш email",
            "autocomplete": "email",
            "class": "newsletter_input"
        })
    )