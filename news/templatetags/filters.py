from django import template

register = template.Library()  

@register.filter(name='multiply')  
def multiply(value, arg):  
    return str(value) * arg  


CENSORED = ["стопслово1", "стопслово2", "стопслово3"]


@register.filter(name='censor')
def censor(value):
    text = value.split()
    for word in text:
        if word.lower() in CENSORED:
            value = value.replace(word, '****')
    return value
