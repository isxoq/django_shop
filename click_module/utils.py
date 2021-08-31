import json

import requests
from django.utils.translation import ugettext_lazy as _
from payments import PaymentStatus
from payments import get_payment_model
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
import hashlib


def isset(data, columns):
    for column in columns:
        if data.get(column, None):
            return False
    return True


def order_load(payment_id):
    if int(payment_id) > 1000000000:
        return None
    payment = get_object_or_404(get_payment_model(), id=int(payment_id))
    return payment


def click_secret_key():
    PAYMENT_VARIANTS = settings.PAYMENT_VARIANTS
    _click = PAYMENT_VARIANTS['click']
    secret_key = _click[1]['secret_key']
    return secret_key


def click_webhook_errors(data):
    click_trans_id = data['click_trans_id']
    service_id = data['service_id']
    click_paydoc_id = data['click_paydoc_id']
    order_id = data['merchant_trans_id']
    amount = data['amount']
    action = data['action']
    error = data['error']
    error_note = data['error_note']
    sign_time = data['sign_time']
    sign_string = data['sign_string']
    merchant_prepare_id = data['merchant_prepare_id'] if action != None and action == '1' else ''

    if isset(data,
             ['click_trans_id', 'service_id', 'click_paydoc_id', 'amount', 'action', 'error', 'error_note', 'sign_time',
              'sign_string']) or (
            action == '1' and isset(data, ['merchant_prepare_id'])):
        return {
            'error': '-8',
            'error_note': _('Error in request from click')
        }

    signString = '{}{}{}{}{}{}{}{}'.format(
        click_trans_id, service_id, click_secret_key(), order_id, merchant_prepare_id, amount, action, sign_time
    )
    encoder = hashlib.md5(signString.encode('utf-8'))
    signString = encoder.hexdigest()
    if signString != sign_string:
        return {
            'error': '-1',
            'error_note': _('SIGN CHECK FAILED!')
        }

    if action not in ['0', '1']:
        return {
            'error': '-3',
            'error_note': _('Action not found')
        }

    order = order_load(order_id)
    if not order:
        return {
            'error': '-5',
            'error_note': _('User does not exist')
        }

    if abs(float(amount) - float(order.total) > 0.01):
        return {
            'error': '-2',
            'error_note': _('Incorrect parameter amount')
        }

    if order.status == PaymentStatus.CONFIRMED:
        return {
            'error': '-4',
            'error_note': _('Already paid')
        }

    if action == '1':
        if order_id != merchant_prepare_id:
            return {
                'error': '-6',
                'error_note': _('Transaction not found')
            }

    if order.status == PaymentStatus.REJECTED or int(error) < 0:
        return {
            'error': '-9',
            'error_note': _('Transaction cancelled')
        }

    return {
        'error': '0',
        'error_note': 'Success'
    }


def prepare(request):
    data = json.loads(request.body.decode('utf-8'))

    order_id = data['merchant_trans_id']

    result = click_webhook_errors(data)
    order = order_load(order_id)
    if result['error'] == '0':
        order.status = PaymentStatus.WAITING
        order.save()
    result['click_trans_id'] = data['click_trans_id']
    result['merchant_trans_id'] = data['merchant_trans_id']
    result['merchant_prepare_id'] = data['merchant_trans_id']
    result['merchant_confirm_id'] = data['merchant_trans_id']

    return JsonResponse(result)


def complete(request):
    data = json.loads(request.body.decode('utf-8'))

    order_id = data['merchant_trans_id']
    order = order_load(order_id)
    result = click_webhook_errors(data)
    if data['error'] is not None and int(data['error']) < 0:
        order.status = PaymentStatus.REJECTED
    order.save()
    if result['error'] == '0':
        order.status = PaymentStatus.CONFIRMED
    order.save()
    result['click_trans_id'] = data['click_trans_id']
    result['merchant_trans_id'] = data['merchant_trans_id']
    result['merchant_prepare_id'] = data['merchant_prepare_id']
    result['merchant_confirm_id'] = data['merchant_prepare_id']
    return JsonResponse(result)
