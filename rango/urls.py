from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    
    path('about/', views.AboutView.as_view(), name='about'),

    path('contact_us/', views.contact_us, name='contact_us'),

    path('register_profile/', views.RegisterProfileView.as_view(), name='register_profile'),

    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),

    path('delete/<username>', views.delete_account, name='delete_account'),

    path('profiles/', views.ListProfilesView.as_view(), name='list_profiles'),

    path('search/', views.SearchResultsView.as_view(), name='search_results'),

    path('add_book/', views.AddBookView.as_view(), name='add_book'),

    path('books/', views.list_books, name='books'),

    path('like_review/', views.LikeReviewView.as_view(), name='like_review'),

    path('dislike_review/', views.DislikeReviewView.as_view(), name='dislike_review'),

    path('<slug:book_title_slug>/', views.ShowBookView.as_view(), name='show_book'),

    path('<slug:book_title_slug>/leave_review/',
         views.LeaveReviewView.as_view(), name='leave_review'),

]