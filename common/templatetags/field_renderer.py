from django import template

register = template.Library()

@register.simple_tag
def field(boundfield, attrs):
    attrs = attrs.split(",")
    att = {}
    for attr in attrs:
        splitted = attr.split("=")
        att[splitted[0]] = ""
        if len(splitted) > 1: att[splitted[0]] = splitted[1]

    if boundfield.field.show_hidden_initial:
        return boundfield.as_widget(attrs=att) + boundfield.as_hidden(only_initial=True)
    return boundfield.as_widget(attrs=att)