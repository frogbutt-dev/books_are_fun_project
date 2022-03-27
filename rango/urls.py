from django.urls import path
from rango import views
from .views import SearchResultsView

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    
    path('about/', views.AboutView.as_view(), name='about'),

    path('contact_us/', views.contact_us, name='contact_us'),

    path('register_profile/', views.register_profile, name='register_profile'),

    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),

    path('delete/<username>', views.delete_account, name='delete_account'),

    path('profiles/', views.ListProfilesView.as_view(), name='list_profiles'),

    path('search/', SearchResultsView.as_view(), name='search_results'),

    path('add_book/', views.AddBookView.as_view(), name='add_book'),

    path('books/', views.list_books, name='books'),

    path('<slug:book_title_slug>/', views.show_book, name='show_book'),

    path('<slug:book_title_slug>/leave_review/',
         views.leave_review, name='leave_review'),

]