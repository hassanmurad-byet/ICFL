from django import template

register = template.Library()

@register.filter(name='time_format')
def time_format(value):
    minutes = int(value // 60)
    seconds = int(value % 60)
    return f"{minutes}:{str(seconds).zfill(2)}"