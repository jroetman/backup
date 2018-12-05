from django import template
register = template.Library()
print("asdfasdfasdf")

@register.filter(name='split_str')
def split_str(val):
    return val.split(",")
