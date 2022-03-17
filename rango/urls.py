from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    #path('contact_us/', views.contact_us, name='contact_us'),
    #path('upload_book/', views.upload_book, name='upload_book'),
    #path('book/<slug:book_title_slug>/', views.show_book, name='show_book'),
    #path('<slug:book_title_slug>/upload_review/',
    #     views.upload_review, name='upload_review'),
]

