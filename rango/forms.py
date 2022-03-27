from django import forms
from rango.models import Review, Book, UserProfile
from django.contrib.auth.models import User


class BookForm(forms.ModelForm):
    title = forms.CharField(max_length=Book.TITLE_MAX_LENGTH,
                            help_text="Please enter the book title.")

    isbn = forms.CharField(max_length=Book.ISBN_MAX_LENGTH,
                           help_text="Please enter the book ISBN.")

    description = forms.CharField(max_length=Book.DESC_MAX_LENGTH,
                                  help_text="Please enter the book description.")

    author = forms.CharField(max_length=Book.AUTHOR_MAX_LENGTH,
                             help_text="Please enter the book author.")

    publisher = forms.CharField(max_length=Book.PUB_MAX_LENGTH,
                                help_text="Please enter the book publisher.")

    language = forms.CharField(max_length=Book.LANG_MAX_LENGTH,
                               help_text="Please enter the book language.")

    price = forms.DecimalField(help_text="Please enter the book price.")

    class Meta:
        model = Book
        fields = ('title', 'isbn', 'description', 'author', 'publisher', 'language', 'price', )


class ReviewForm(forms.ModelForm):
    title = forms.CharField(max_length=Review.TITLE_MAX_LENGTH,
                            help_text="Please enter the review title.")

    rating = forms.IntegerField(help_text="Please enter a rating out of 5 stars.")

    comment = forms.CharField(max_length=Review.COMM_MAX_LENGTH,
                              help_text="Please enter a comment (optional).")

    genre = forms.CharField(max_length=Review.GENRE_MAX_LENGTH,
                            help_text="Please enter the book genre.")

    class Meta:
        model = Review
        exclude = ['book', 'publishDate', 'upvotes', 'slug', ]


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
