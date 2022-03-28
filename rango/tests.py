from venv import create
from django.test import TestCase
from rango.models import Book, Review, UserProfile
from django.urls import reverse
from django.contrib.auth.models import User



class BookMethodTests(TestCase):
    def test_ensure_price_is_non_zero(self):
        book = Book(title='test', price=10)
        book.save()
        self.assertEqual((Book.price != 0), True)
    
    def test_slug_line_creation(self):
        book = Book(title='Random Book String')
        book.save()
        self.assertEqual(book.slug, 'random-book-string')


class IndexViewTests(TestCase):
    def test_index_view_with_no_books_status(self):
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_with_no_books_string(self):
        response = self.client.get(reverse('rango:index'))
        self.assertContains(response, 'There are no books present.')
    
    def test_index_view_with_no_books_context(self):
        response = self.client.get(reverse('rango:index'))
        self.assertQuerysetEqual(response.context['books'], [])
    
    def test_index_view_with_books_status(self):
        add_book('Harry Potter')
        add_book('Shrek')
        add_book('Naruto')
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_with_books_titles(self):
        add_book('Harry Potter')
        add_book('Shrek')
        add_book('Naruto')
        response = self.client.get(reverse('rango:index'))
        self.assertContains(response, "Harry Potter")
        self.assertContains(response, "Shrek")
        self.assertContains(response, "Naruto")

    def test_index_view_with_books_count(self):
        add_book('Harry Potter')
        add_book('Shrek')
        add_book('Naruto')
        response = self.client.get(reverse('rango:index'))
        num_books = len(response.context['books'])
        self.assertEquals(num_books, 3)


class ShowBookViewTests(TestCase):
    def test_show_book_view_displays_correct_score_status(self):
        book_one = add_book("Flying Donkey")
        user_one_name, user_two_name = "Jerry", "Tom"
        user_one_pw, user_two_pw = "tompassword123", "tompassword123"
        leave_review(book_one, create_user(user_one_name, user_one_pw, self), "Boring story", 3)
        leave_review(book_one, create_user(user_two_name, user_two_pw, self), "Awesome story", 5)
        response = self.client.get(reverse('rango:show_book', kwargs={'book_title_slug': book_one.slug}))
        self.assertEqual(response.status_code, 200)
    
    def test_show_book_view_displays_correct_score(self):
        book_one = add_book("Flying Donkey")
        user_one_name, user_two_name = "Jerry", "Tom"
        user_one_pw, user_two_pw = "tompassword123", "tompassword123"
        leave_review(book_one, create_user(user_one_name, user_one_pw, self), "Boring story", 3)
        leave_review(book_one, create_user(user_two_name, user_two_pw, self), "Awesome story", 5)
        response = self.client.get(reverse('rango:show_book', kwargs={'book_title_slug': book_one.slug}))
        self.assertContains(response, 4)


class ListProfilesViewTests(TestCase):
    def test_list_profiles_view_with_users_status(self):
        user_one_name, user_two_name = "Jerry", "Tom"
        user_one_pw, user_two_pw = "tompassword123", "tompassword123"
        create_user_profile(user_one_name, user_one_pw, self)
        create_user_profile(user_two_name, user_two_pw, self)
        response = self.client.get(reverse('rango:list_profiles'))
        self.assertEqual(response.status_code, 200)

    def test_list_profiles_view_with_users_count(self):
        user_one_name, user_two_name = "Jerry", "Tom"
        user_one_pw, user_two_pw = "tompassword123", "tompassword123"
        create_user_profile(user_one_name, user_one_pw, self)
        create_user_profile(user_two_name, user_two_pw, self)
        response = self.client.get(reverse('rango:list_profiles'))
        num_profiles = len(response.context['user_profile_list'])
        self.assertEquals(num_profiles, 2)

    def test_list_profiles_view_with_users_names(self):
        user_one_name, user_two_name = "Jerry", "Tom"
        user_one_pw, user_two_pw = "tompassword123", "tompassword123"
        create_user_profile(user_one_name, user_one_pw, self)
        create_user_profile(user_two_name, user_two_pw, self)
        response = self.client.get(reverse('rango:list_profiles'))
        self.assertContains(response, "Jerry")
        self.assertContains(response, "Tom")


class ProfileViewTests(TestCase):
    def test_user_profile_view_with_reviews_status(self):
        book_one = add_book('Naruto')
        book_two = add_book('Mr Bean')
        user_one = create_user_profile("Mario", "mariopassword123", self)
        leave_review(book_one, user_one.user, "Enjoyed it", 4)
        leave_review(book_two, user_one.user, "Meh...", 2)
        response = self.client.get(reverse('rango:profile', kwargs={'username': user_one.user.username}))
        self.assertEqual(response.status_code, 200)

    def test_user_profile_view_with_reviews_count(self):
        book_one = add_book('Naruto')
        book_two = add_book('Mr Bean')
        user_one = create_user_profile("Mario", "mariopassword123", self)
        leave_review(book_one, user_one.user, "Enjoyed it", 4)
        leave_review(book_two, user_one.user, "Meh...", 2)
        response = self.client.get(reverse('rango:profile', kwargs={'username': user_one.user.username}))
        num_reviews = len(response.context['reviews'])
        self.assertEquals(num_reviews, 2)


class LeaveReviewViewTests(TestCase):
    def test_review_view_with_book_status(self):
        book_one = add_book('Naruto')
        create_user("john", "johnpassword123", self)
        response = self.client.get(reverse('rango:leave_review', kwargs={'book_title_slug': book_one.slug}))
        self.assertEqual(response.status_code, 200)

    def test_review_view_with_book_slug(self):
        book_one = add_book('Naruto')
        create_user("john", "johnpassword123", self)
        response = self.client.get(reverse('rango:leave_review', kwargs={'book_title_slug': book_one.slug}))
        self.assertContains(response, book_one.slug)




# Helper Methods

def add_book(title):
    book = Book.objects.get_or_create(title=title)[0]
    book.save()
    return book

def leave_review(book, user, title, rating):
    review = Review.objects.get_or_create(book=book, title=title, user=user)[0]
    review.rating = rating
    return review

def create_user(username, password, self):
    my_user = User.objects.create_user(username=username, password=password)
    my_user.save()
    self.client.login(username=username, password=password)
    return my_user

def create_user_profile(username, password, self):
    user = create_user(username, password, self)
    user = UserProfile.objects.get_or_create(user=user)[0]
    user.save()
    return user