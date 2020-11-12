from django import template

register = template.Library()


@register.filter(name='ru_plural', is_safe=False)
def ru_pluralize(value, arg=''):
    """
    Выбирает правильную форму множественного числа в русском языке
    Принимает число и три формы существительного в строке через запятую
        первое слово в строке для единственного числа,
        второе для 2,3,4 предметов
        третье для множественного числа (0, 5 и более)
    """
    try:
        nouns = arg.split(',')
    except AttributeError:
        return ''
    nouns.extend(['', '', ''])
    one, few, many = nouns[:3]
    try:
        n = abs(value)
    except TypeError:
        return ''
    if n % 10 == 1 and n % 100 != 11:
        noun = one
    elif n % 10 in [0, 5, 6, 7, 8, 9] or n % 100 in [11, 12, 13, 14]:
        noun = many
    else:
        noun = few
    return noun

@register.filter(name='creation_time_str', is_safe=True)
def creation_time(obj):
    """
    Шоткат. на вход принимает объект с полем creation_time
    на выходе форматированная строка с датой и временем создания объекта
    """
    from django.template.defaultfilters import date, time
    obj = obj.creation_time
    return f'{date(obj, "d M")} \'{date(obj, "y")} в {time(obj, "H:i")}'
