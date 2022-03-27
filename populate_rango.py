from asyncio.windows_events import NULL
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

    reviewForBookFour = [
        {'title': 'I loooved it',
         'rating': 1,
         'comment': 'I did not enjoy reading this book. It was very boring.',
         'genre': 'Romantic',
         'publishDate': datetime.date(2008, 10, 1),
         'upvotes': 3, },
    ]

    reviewForBookFive = [
        {'title': 'Amazing. I became Buddha.',
         'rating': 5,
         'comment': 'The colours on the cover enlightened me.',
         'genre': 'Therapy',
         'publishDate': datetime.date(1997, 10, 19),
         'upvotes': 500, },
    ]

    reviewForBookSix = [
        {'title': 'Mid',
         'rating': 3,
         'comment': 'I did not like it or dislike it. One Piece is better.',
         'genre': 'Adventure',
         'publishDate': datetime.date(2000, 1, 5),
         'upvotes': 25, },
    ]

    books = {'Before The Coffee Gets Cold': 
             {'reviews': reviewForBookOne, 
              'bookPicture': None, 
              'isbn': '9781529029581', 
              'description': 'What would you do if you knew there were creepy robots with shocking habits near the ones you love? The night of the Christening changes everything for Rachel Sparrow, a 24-year-old doctor from New York. One moment, she is discussing sausages with her hilarious friend, Sandie Raymond; the next, watching with horror as creepy robots punch each other. She knows these robots came from Falmouth but she can\'t prove it - at least not without some dirty wigs. The intuitive, friendly woman knows that her quiet life is over. She acquires some dirty wigs and is reborn as the hero who will save the world from creepy robots. However, Rachel finds herself troubled by her quiet ideals and becomes overwhelmed with moral questions. Will her conscience allow her to do whatever is needed to stop the creepy robots?', 
              'author': 'Toshikazu Kawaguchi', 
              'publisher': 'Picador', 
              'price': 10, 
              'language': 'English',
              'score' : 5.0},
             'At Night All Blood is Black':
                 {'reviews': reviewForBookTwo, 
                  'bookPicture': None, 
                  'isbn': '9780374266974', 
                  'description': 'What would you do if you knew there were creepy robots with shocking habits near the ones you love? The night of the Christening changes everything for Rachel Sparrow, a 24-year-old doctor from New York. One moment, she is discussing sausages with her hilarious friend, Sandie Raymond; the next, watching with horror as creepy robots punch each other. She knows these robots came from Falmouth but she can\'t prove it - at least not without some dirty wigs. The intuitive, friendly woman knows that her quiet life is over. She acquires some dirty wigs and is reborn as the hero who will save the world from creepy robots. However, Rachel finds herself troubled by her quiet ideals and becomes overwhelmed with moral questions. Will her conscience allow her to do whatever is needed to stop the creepy robots?', 
                  'author': 'David Diop', 
                  'publisher': 'Pushkin Press', 
                  'price': 9,  
                  'language': 'English',
                  'score' : 2.5},
             'The 100-Year-Old Man Who Climbed Out the Window and Disappeared': 
                 {'reviews': reviewForBookThree, 
                  'bookPicture': None,
                  'isbn': '9780786891450', 
                  'description': 'What would you do if you knew there were creepy robots with shocking habits near the ones you love? The night of the Christening changes everything for Rachel Sparrow, a 24-year-old doctor from New York. One moment, she is discussing sausages with her hilarious friend, Sandie Raymond; the next, watching with horror as creepy robots punch each other. She knows these robots came from Falmouth but she can\'t prove it - at least not without some dirty wigs. The intuitive, friendly woman knows that her quiet life is over. She acquires some dirty wigs and is reborn as the hero who will save the world from creepy robots. However, Rachel finds herself troubled by her quiet ideals and becomes overwhelmed with moral questions. Will her conscience allow her to do whatever is needed to stop the creepy robots?', 
                  'author': 'Jonas Jonasson', 
                  'publisher': 'Hyperion', 
                  'price': 8, 
                  'language': 'English',
                  'score' : 3.0},
             'It Ends With Us': 
                 {'reviews': reviewForBookFour, 
                  'bookPicture': None,
                  'isbn': '9781471156267', 
                  'description': 'SOMETIMES THE ONE WHO LOVES YOU IS THE ONE WHO HURTS YOU THE MOST.', 
                  'author': 'Colleen Hoover', 
                  'publisher': 'Simon & Schuster UK', 
                  'price': 5, 
                  'language': 'English',
                  'score' : 4.0},
             'Why Has Nobody Told Me This Before?': 
                 {'reviews': reviewForBookFive, 
                  'bookPicture': None,
                  'isbn': '9780241529713', 
                  'description': "Drawing on years of experience as a clinical psychologist, online sensation Dr Julie Smith shares all the skills you need to get through life's ups and downs.", 
                  'author': 'Dr Julie Smith', 
                  'publisher': 'Michael Joseph', 
                  'price': 7.49, 
                  'language': 'English',
                  'score' : 3.5},
             'Naruto Volume 1': 
                 {'reviews': reviewForBookSix, 
                  'bookPicture': None,
                  'isbn': '9781569319000', 
                  'description': 'Twelve years ago the Village Hidden in the Leaves was attacked by a fearsome threat. A nine-tailed fox spirit claimed the life of the village leader, the Hokage, and many others. Today, the village is at peace and a troublemaking kid named Naruto is struggling to graduate from Ninja Academy. His goal may be to become the next Hokage, but his true destiny will be much more complicated. The adventure begins now! For teen audiences.', 
                  'author': 'Masashi Kishimoto', 
                  'publisher': 'Viz LLC', 
                  'price': 6.99, 
                  'language': 'English',
                  'score' : 4.5},
             }


    for book, book_data in books.items():
        b = add_book(book, 
            book_data['isbn'], 
            book_data['description'], 
            book_data['author'], 
            book_data['publisher'], 
            book_data['price'], 
            book_data['language'],
            book_data['score'],)
        
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


def add_book(title, isbn, description, author, publisher, price, language, score):
    b = Book.objects.get_or_create(title=title, 
        isbn=isbn, 
        description=description, 
        author=author, 
        publisher=publisher, 
        price=price, 
        language=language,
        score=score,)[0]
    b.save()
    return b


# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()