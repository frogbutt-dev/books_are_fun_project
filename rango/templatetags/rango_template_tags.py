from django import template
from rango.models import Book

register = template.Library()

@register.inclusion_tag('rango/books.html')
def get_book_list(current_book=None):
    return {'books': Book.objects.all(),
            'current_book': current_book}
