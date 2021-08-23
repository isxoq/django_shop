from django import forms


class SignUpForm(forms.Form):
    phone = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()


class VerifyCode(forms.Form):
    code = forms.IntegerField()
