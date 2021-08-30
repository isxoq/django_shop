from django import forms


class OrderForm(forms.Form):
    phone = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
