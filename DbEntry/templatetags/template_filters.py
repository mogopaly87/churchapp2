from django import template
register = template.Library()


'''This custom filter receives the pre-populated phone number in the 
format (000)000-0000. The function then removes the unwanted characters.
Then it returns/presents the pre-populated number in the format 000-000-0000 '''
@register.filter(name='phone_number')
def phone_number(number):
    
    bad_xters = [')', '(', ' ', '-']

    for i in bad_xters:
        number = str(number).replace(i, '')

    first = number[0:3]
    second = number[3:6]
    third = number[6:10]

    return (first + '-' + second + '-' + third)