# Generated by Django 2.2.26 on 2022-03-27 04:45

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=13, validators=[django.core.validators.MinLengthValidator(13)])),
                ('title', models.CharField(max_length=128, unique=True)),
                ('description', models.CharField(max_length=1000)),
                ('author', models.CharField(max_length=50)),
                ('publisher', models.CharField(max_length=50)),
                ('language', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bookPicture', models.ImageField(blank=True, upload_to='')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, upload_to='')),
                ('joinDate', models.DateField(default=datetime.date.today)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('rating', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.CharField(blank=True, max_length=100)),
                ('genre', models.CharField(max_length=50)),
                ('publishDate', models.DateField(default=datetime.date.today)),
                ('upvotes', models.IntegerField(default=0)),
                ('slug', models.SlugField(unique=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rango.Book')),
            ],
        ),
    ]
