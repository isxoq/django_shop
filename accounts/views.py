import time

from django.shortcuts import render, redirect
from .forms import SignUpForm, VerifyCode
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .models import TempNumber
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def send_sms(phone):
    # Logic
    return 12345678


def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    modelForm = SignUpForm()

    if request.POST:
        modelForm = SignUpForm(request.POST)
        if modelForm.is_valid():
            send_sms_code(request.POST)
            return redirect('verify', phone=request.POST.get('phone'))

    return render(request, 'register.html', {
        "form": modelForm
    })


def verify(request, phone):
    verifyForm = VerifyCode()

    if request.POST:
        verifyForm = VerifyCode(request.POST)
        if verifyForm.is_valid():
            print("POST")
            try:
                temp_number = TempNumber.objects.get(phone=phone)
                if temp_number.code == int(request.POST.get('code')):
                    user = User.objects.create_user(temp_number.phone, temp_number.email, "12345678")
                    user.save()
                    temp_number.delete()

                    login(request, user)

                    return redirect('index')
                else:
                    verifyForm.add_error('code', "Kod notog'ri")
            except ObjectDoesNotExist:
                print("asds")
        else:
            print("invalid")
            print(request.POST.get('code'))

    return render(request, 'verify.html', {
        "form": verifyForm
    })


def send_sms_code(data):
    try:
        temp_phone = TempNumber.objects.get(phone=data.get('phone'))
        if time.time() >= temp_phone.expire_at:

            temp_phone.code = 777777
            temp_phone.expire_at = time.time() + 120
            temp_phone.save()
        else:
            print(temp_phone)

    except ObjectDoesNotExist:
        temp_phone = TempNumber.objects.create(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone=data.get('phone'),
            email=data.get('email'),
            code=12345678,
            expire_at=time.time() + 120
        )
        temp_phone.save()
