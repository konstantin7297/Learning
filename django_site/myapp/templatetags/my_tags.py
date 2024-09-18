from django import template
from myapp.models import Product


register = template.Library()  # Через него регистрируем собственные шаблонные теги.


@register.simple_tag(name="my_simple_tag")  # name - имя тега в шаблоне.
def my_simple_tag(pk):  # Пример использования в шаблоне '2-rule.html'.
    """ Функция показывает, как можно сделать одиночный тег. Просто вызывается в шаблоне как переменная, но без имени. С ней нельзя работать изначально. """
    return Product.objects.filter(pk=pk)  # Что бы обратиться к этой переменной, ей нужно дать имя: {% my_simple_tag as my_tag_name %}


@register.inclusion_tag("myapp/2-rule.html")  # Указывается шаблон, в котором должен быть доступен этот тег.
def my_inclusion_tag(pk):  # Пример использования в шаблоне '2-rule.html'.
    """ Функция показывает, как можно сделать встроенный тег. В примере он отображается в доп файле: '6-template_tags.html', но вызывается в: '2-rule.html'. """
    return {"tag1": Product.objects.filter(pk=pk)}
