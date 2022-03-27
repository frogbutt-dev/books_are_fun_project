import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    # FK Relationships

    # Max Length Values
    ISBN_MAX_LENGTH = 13
    TITLE_MAX_LENGTH = 128
    DESC_MAX_LENGTH = 1000
    AUTHOR_MAX_LENGTH = 50
    PUB_MAX_LENGTH = 50
    LANG_MAX_LENGTH = 50
    SCORE_MAX_LENGTH = 50

    # Attributes
    isbn = models.CharField(max_length=ISBN_MAX_LENGTH)
    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True)
    description = models.TextField(max_length=DESC_MAX_LENGTH)
    author = models.CharField(max_length=AUTHOR_MAX_LENGTH)
    publisher = models.CharField(max_length=PUB_MAX_LENGTH)
    language = models.CharField(max_length=LANG_MAX_LENGTH)
    price = models.IntegerField(default=0)
    bookPicture = models.ImageField(blank=True)
    score = models.FloatField(default=0)

    # Slug
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)

    # To string
    def __str__(self):
        return self.title


class Review(models.Model):
    # FK Relationships
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    # Max Length Values
    TITLE_MAX_LENGTH = 50
    COMM_MAX_LENGTH = 1000
    GENRE_MAX_LENGTH = 50

    # Attributes
    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True)
    rating = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(max_length=COMM_MAX_LENGTH, blank=True)
    genre = models.TextField(max_length=GENRE_MAX_LENGTH)
    publishDate = models.DateField(default=datetime.date.today)
    upvotes = models.IntegerField(default=0)

    # Slug
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Review, self).save(*args, **kwargs)

    
    # To string
    def __str__(self):
        return self.title


class UserProfile(models.Model):
    # FK Relationships
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Attributes
    picture = models.ImageField(blank=True)
    joinDate = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.user.username