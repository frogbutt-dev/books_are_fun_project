from django.contrib import admin
from rango.models import Book, Review, UserProfile


admin.site.register(Book)
admin.site.register(Review)
admin.site.register(UserProfile)