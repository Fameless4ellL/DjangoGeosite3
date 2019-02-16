from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Paginator
    используется для коприрование ссылки, и вставлялось в адресную строку вместе с остальными командами в ней

    Пример:
    http://127.0.0.1:8000/?csrfmiddlewaretoken=ITlYTRZjBewIKNpMhzCX0pE02mauXzx4Lafx93MCRi8v2jZLoTaS0M930cXZSX8s&tags=2&tags=1&page=2
    вместо:
    http://127.0.0.1:8000/?page=2

    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.filter()
def to_class_name(value):
    return value.__class__.__name__
