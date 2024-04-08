from django import template
from datetime import datetime
from django.utils.encoding import force_str


register = template.Library()


@register.filter
def format_lao_date(value):
    if isinstance(value, datetime):
        # Format with 12-hour clock and AM/PM indicator
        return value.strftime('%d/%m/%Y %I:%M %p')
    else:
        return value


@register.filter(name='intcomma')
def intcomma(value):
    value = force_str(value)
    parts = []
    if '.' in value:
        int_part, dec_part = value.split('.')
    else:
        int_part, dec_part = value, None
    while int_part:
        int_part, last_part = int_part[:-3], int_part[-3:]
        parts.append(last_part)
    int_part = ','.join(reversed(parts))
    if dec_part:
        return f'{int_part}.{dec_part}'
    return int_part
