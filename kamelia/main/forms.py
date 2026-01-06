from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import Subscriber, RoomBooking
from dal import autocomplete
from allauth.account.forms import LoginForm, ResetPasswordForm
from django.utils import timezone
from datetime import date


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
    


class AvailabilitySearchForm(forms.Form):
    checkin = forms.DateField(
        label="Заезд",
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "class": "form-control js-date",
                "id": "checkin_date",
                "autocomplete": "off",
                "placeholder": "YYYY-MM-DD",
                "type": "text",
            }
        )
    )
    checkout = forms.DateField(
        label="Выезд",
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "class": "form-control js-date",
                "id": "checkout_date",
                "autocomplete": "off",
                "placeholder": "YYYY-MM-DD",
                "type": "text",
            }
        )
    )
    adults = forms.IntegerField(
        label="Взрослые",
        min_value=1,
        initial=2,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1})
    )
    children = forms.IntegerField(
        label="Дети",
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 0})
    )

    def clean(self):
        cleaned = super().clean()
        checkin = cleaned.get("checkin")
        checkout = cleaned.get("checkout")
        if checkin and checkout and checkout <= checkin:
            raise forms.ValidationError("Дата выезда должна быть позже даты заезда.")
        return cleaned




class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = RoomBooking
        fields = ("guest_name", "guest_phone", "guest_email", "comment")
        widgets = {
            "guest_name": forms.TextInput(attrs={"class": "form-control"}),
            "guest_phone": forms.TextInput(attrs={"class": "form-control"}),
            "guest_email": forms.EmailInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
