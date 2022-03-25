import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'books_are_fun_project.settings')

import django
django.setup()
import datetime
from rango.models import Book, Review


def populate():

    reviewForBookOne = [
        {'title': 'Fantastic read',
         'rating': 4,
         'comment': 'The story took me back to my childhood.',
         'genre': 'Horror',
         'publishDate': datetime.date(1997, 10, 19),
         'upvotes': 11, },
        {'title': 'Highly interesting',
         'rating': 5,
         'comment': 'A very interesting book.',
         'genre': 'Horror',
         'publishDate': datetime.date(1997, 10, 21),
         'upvotes': 3, },
    ]

    reviewForBookTwo = [
        {'title': 'Brilliant book',
         'rating': 5,
         'comment': 'I loved reading it!',
         'genre': 'Sci-fi',
         'publishDate': datetime.date(1997, 10, 19),
         'upvotes': 23, },
    ]

    reviewForBookThree = [
        {'title': 'Boring story',
         'rating': 2,
         'comment': 'I did not enjoy reading this book. It was very boring.',
         'genre': 'Romantic',
         'publishDate': datetime.date(1997, 10, 19),
         'upvotes': 0, },
    ]

    books = {'Before The Coffee Gets Cold': 
             {'reviews': reviewForBookOne, 
              'bookPicture': None, 
              'isbn': '9781529029581', 
              'description': 'What would you do if you knew there were creepy robots with shocking habits near the ones you love? The night of the Christening changes everything for Rachel Sparrow, a 24-year-old doctor from New York. One moment, she is discussing sausages with her hilarious friend, Sandie Raymond; the next, watching with horror as creepy robots punch each other. She knows these robots came from Falmouth but she can\'t prove it - at least not without some dirty wigs. The intuitive, friendly woman knows that her quiet life is over. She acquires some dirty wigs and is reborn as the hero who will save the world from creepy robots. However, Rachel finds herself troubled by her quiet ideals and becomes overwhelmed with moral questions. Will her conscience allow her to do whatever is needed to stop the creepy robots?', 
              'author': 'Toshikazu Kawaguchi', 
              'publisher': 'Picador', 
              'price': 10, 
              'language': 'English'},
             'At Night All Blood is Black':
                 {'reviews': reviewForBookTwo, 
                  'bookPicture': None, 
                  'isbn': '9780374266974', 
                  'description': 'What would you do if you knew there were creepy robots with shocking habits near the ones you love? The night of the Christening changes everything for Rachel Sparrow, a 24-year-old doctor from New York. One moment, she is discussing sausages with her hilarious friend, Sandie Raymond; the next, watching with horror as creepy robots punch each other. She knows these robots came from Falmouth but she can\'t prove it - at least not without some dirty wigs. The intuitive, friendly woman knows that her quiet life is over. She acquires some dirty wigs and is reborn as the hero who will save the world from creepy robots. However, Rachel finds herself troubled by her quiet ideals and becomes overwhelmed with moral questions. Will her conscience allow her to do whatever is needed to stop the creepy robots?', 
                  'author': 'David Diop', 
                  'publisher': 'Pushkin Press', 
                  'price': 9,  
                  'language': 'English'},
             'The 100-Year-Old Man Who Climbed Out the Window and Disappeared': 
                 {'reviews': reviewForBookThree, 
                  'bookPicture': None,
                  'isbn': '9780786891450', 
                  'description': 'What would you do if you knew there were creepy robots with shocking habits near the ones you love? The night of the Christening changes everything for Rachel Sparrow, a 24-year-old doctor from New York. One moment, she is discussing sausages with her hilarious friend, Sandie Raymond; the next, watching with horror as creepy robots punch each other. She knows these robots came from Falmouth but she can\'t prove it - at least not without some dirty wigs. The intuitive, friendly woman knows that her quiet life is over. She acquires some dirty wigs and is reborn as the hero who will save the world from creepy robots. However, Rachel finds herself troubled by her quiet ideals and becomes overwhelmed with moral questions. Will her conscience allow her to do whatever is needed to stop the creepy robots?', 
                  'author': 'Jonas Jonasson', 
                  'publisher': 'Hyperion', 
                  'price': 8, 
                  'language': 'English'},
             }


    for book, book_data in books.items():
        b = add_book(book, 
            book_data['isbn'], 
            book_data['description'], 
            book_data['author'], 
            book_data['publisher'], 
            book_data['price'], 
            book_data['language'],)
        
        for r in book_data['reviews']:
            add_review(b, r['title'], r['rating'], r['comment'], r['genre'], r['publishDate'], r['upvotes'],)

    # Print out the books we have added.
    for b in Book.objects.all():
        for r in Review.objects.filter(book=b):
            print(f'- {b}: {r}')


def add_review(book, title, rating, comment, genre, publishDate, upvotes):
    r = Review.objects.get_or_create(book=book, title=title)[0]
    r.rating = rating
    r.comment = comment
    r.genre = genre
    r.publishDate = publishDate
    r.upvotes = upvotes
    r.save()
    return r


def add_book(title, isbn, description, author, publisher, price, language):
    b = Book.objects.get_or_create(title=title, 
        isbn=isbn, 
        description=description, 
        author=author, 
        publisher=publisher, 
        price=price, 
        language=language)[0]
    b.save()
    return b


# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()