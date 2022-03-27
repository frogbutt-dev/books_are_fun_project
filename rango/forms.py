from django import forms
from rango.models import Review, Book, UserProfile
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


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

    price = forms.IntegerField(initial=0,
                                    help_text="Please enter the book price.")

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Book
        fields = ('title',)


class ReviewForm(forms.ModelForm):
    title = forms.CharField(max_length=Review.TITLE_MAX_LENGTH, help_text="Enter a title for your review")
    rating = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = forms.CharField(widget=forms.Textarea, max_length=Review.COMM_MAX_LENGTH, help_text="Enter your review")
    
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Review

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values; we may not want to include them.
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        #exclude = ('category',)
        # or specify the fields to include (don't include the category field).
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