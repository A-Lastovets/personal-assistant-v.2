from django import template

register = template.Library()


@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})


@register.filter(name='add_attrs')
def add_attrs(field, attrs_string):
    attrs = {}

    if isinstance(attrs_string, str):
        args = attrs_string.split(',')
        if len(args) > 0:
            attrs["class"] = args[0].strip()
        if len(args) > 1:
            try:

                attrs["rows"] = int(args[1].strip())
            except ValueError:
                attrs["rows"] = None

    return field.as_widget(attrs=attrs)
