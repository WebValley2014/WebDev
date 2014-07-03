__author__ = 'michele'

from django.conf import settings

def get_bootsrap_badge(status):
    if status == 'SUCCESS':
        badge = 'label-success'
    elif status == 'STARTED' or status == 'RUNNING':
        badge = 'label-primary'
    elif status == 'RETRY':
        badge = 'label-default'
    elif status == 'FAILURE':
        badge = 'label-danger'
    elif status == 'PENDING':
        badge = 'label-default'
    else:
        badge = 'label-default'

    return badge

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
