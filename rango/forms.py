from django import forms
from rango.models import Review, Book, UserProfile
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, int_list_validator


class BookForm(forms.ModelForm):
    title = forms.CharField(max_length=Book.TITLE_MAX_LENGTH,
                                    help_text="Please enter the book title.")

    isbn = forms.CharField(validators=[MinLengthValidator(13), int_list_validator(sep='', message="ISBN consists of only 13 digits")],
                                    max_length=Book.ISBN_MAX_LENGTH, 
                                    help_text="Please enter the book ISBN (must be 13 digits long).")

    description = forms.CharField(widget=forms.Textarea, max_length=Book.DESC_MAX_LENGTH,
                                    help_text="Please enter the book description.")

    author = forms.CharField(max_length=Book.AUTHOR_MAX_LENGTH,
                                    help_text="Please enter the book author.")

    publisher = forms.CharField(max_length=Book.PUB_MAX_LENGTH,
                                    help_text="Please enter the book publisher.")

    language = forms.CharField(max_length=Book.LANG_MAX_LENGTH,
                                    help_text="Please enter the book language.")

    price = forms.DecimalField(help_text="Please enter the book price (without '£').")

    class Meta:
        model = Book
        fields = ('title','isbn', 'description', 'author', 'publisher', 'language', 'price')


class ReviewForm(forms.ModelForm):
    title = forms.CharField(max_length=Review.TITLE_MAX_LENGTH,
                                    help_text="Enter a title for your review")
    
    rating = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],
                                    help_text="Enter a score between 0 and 5")
    
    comment = forms.CharField(widget=forms.Textarea, max_length=Review.COMM_MAX_LENGTH,
                                    help_text="Enter your review")
    
    class Meta:
        model = Review
        fields = ['title', 'rating', 'comment',]


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
