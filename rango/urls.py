from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),

    path('about/', views.about, name='about'),

    path('contact_us/', views.contact_us, name='contact_us'),

    path('add_book/', views.add_book, name='add_book'),

    path('<slug:book_title_slug>/', views.show_book, name='show_book'),

    path('<slug:book_title_slug>/leave_review/',
         views.leave_review, name='leave_review'),

]