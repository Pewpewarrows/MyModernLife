from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

def truncate(value, args='10'):
    """
    Truncates a string after a certain number of characters.

    final_len: Number of characters the final returned value should be,
    after the truncate and string is concatenated.

    str: the string that will be concatenated to the truncated value

    in_middle: whether the value should "wrap" around str, showing the head
    and tail of it
    """
    arglist = args.split(',')
    
    final_len = arglist[0]

    try:
        final_len = int(final_len)
    except ValueError:
        return value

    if len(arglist) > 1:
        str = arglist[1]
    else:
        str = '...'

    if len(arglist) > 2:
        in_middle = arglist[2]
    else:
        in_middle = False

    # I thought I needed the len of the original string at some point...
    # val_len = len(value)
    str_len = len(str)
    trunc_val_len = final_len - str_len

    # Truncated valued must have at least one character remaining, or
    # two in the case of a truncated wrap
    if (not in_middle) and (trunc_val_len < 1):
        return value
    elif in_middle and (trunc_val_len < 2):
        return value

    if not in_middle:
        trunc_val = value[:trunc_val_len] + str
    else:
        from math import floor, ceil
        middle = float(trunc_val_len) / 2
        trunc_val = value[:int(ceil(middle))] + str + value[-int(floor(middle)):]

    return trunc_val
truncate.is_safe = True
truncate = stringfilter(truncate)
register.filter(truncate)
