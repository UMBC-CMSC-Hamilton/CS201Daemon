from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def lookup(dictionary, keys):
    current = dictionary
    keys = keys.split(',')
    for key in keys:
        current = current[key]
    return current
