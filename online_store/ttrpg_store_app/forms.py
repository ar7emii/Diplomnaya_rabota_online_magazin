from django import forms
from .models import *
from django.contrib.auth.models import User
from django.forms import widgets


class CheckOutForm(forms.ModelForm):
    ordered_by = forms.CharField(label="Имя заказчика", widget=widgets.TextInput(
        attrs={"class": "form-control", "type": "text", "placeholder": "Введите имя заказчика"}), )
    shipping_address = forms.CharField(label="Адрес доставки", widget=widgets.TextInput(
        attrs={"class": "form-control", "type": "text", "placeholder": "Введите адрес доставки"}), )
    mobile = forms.CharField(label="Мобильный телефон", widget=widgets.TextInput(
        attrs={"class": "form-control", "type": "tel",
               "placeholder": "Введите мобильный телефон"}), )
    email = forms.EmailField(label="Электронная почта", widget=widgets.TextInput(
        attrs={"type": "email", "class": "form-control", "id": "exampleInputEmail1", "aria-describedby": "emailHelp",
               "placeholder": "Введите электронную почту"}), )

    class Meta:
        model = Order
        fields = ['ordered_by', 'shipping_address', 'mobile', 'email']


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(label="Имя пользователя", widget=widgets.TextInput(
        attrs={"class": "form-control form-control-sm", "type": "text", "placeholder": "Введите имя пользователя"}), )
    password = forms.CharField(label="Пароль", widget=widgets.TextInput(
        attrs={"class": "form-control form-control-sm", "type": "password", "placeholder": "Введите пароль"}), )
    email = forms.CharField(label="Электронная почта", widget=widgets.TextInput(
        attrs={"type": "email", "class": "form-control form-control-sm", "id": "exampleInputEmail1", "aria-describedby": "emailHelp",
               "placeholder": "Введите электронную почту"}), )
    full_name = forms.CharField(label="ФИО", widget=widgets.TextInput(
        attrs={"type": "text", "class": "form-control form-control-sm", "aria-describedby": "emailHelp",
               "placeholder": "Введите ФИО"}), )
    address = forms.CharField(label="Адрес", widget=widgets.TextInput(
        attrs={"class": "form-control form-control-sm", "type": "text", "placeholder": "Введите адрес"}), )

    class Meta:
        model = Customer
        fields = ["username", "password", "email", "full_name", "address"]


class CustomerLoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", widget=widgets.TextInput(
        attrs={"class": "form-control form-control-sm", "type": "text", "placeholder": "Введите имя пользователя"}), )
    password = forms.CharField(label="Пароль", widget=widgets.TextInput(
        attrs={"class": "form-control form-control-sm", "type": "password", "placeholder": "Введите пароль"}), )
