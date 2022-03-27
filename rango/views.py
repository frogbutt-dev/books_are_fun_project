from django.shortcuts import render
from rango.models import Book, Review
from rango.forms import BookForm, ReviewForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from rango.models import UserProfile


def index(request):
    book_list = Book.objects.all()
    review_list = Review.objects.order_by('-upvotes')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'What book are you going to read today?'
    context_dict['books'] = book_list
    context_dict['reviews'] = review_list

    response = render(request, 'rango/index.html', context=context_dict)

    return response


def about(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/about.html', context=context_dict)
    return response


def show_book(request, book_title_slug):
    context_dict = {}
    try:
        book = Book.objects.get(slug=book_title_slug)
        reviews = Review.objects.filter(book=book)
        context_dict['reviews'] = reviews
        context_dict['book'] = book
    except Book.DoesNotExist:
        context_dict['book'] = None
        context_dict['reviews'] = None

    return render(request, 'rango/book.html', context=context_dict)


@login_required
def add_book(request):
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')

        else:
            print(form.errors)

    return render(request, 'rango/add_book.html', {'form': form})


@login_required
def leave_review(request, book_title_slug):
    try:
        book = Book.objects.get(slug=book_title_slug)
    except Book.DoesNotExist:
        book = None

    if book is None:
        return redirect('/rango/')

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            if book:
                review = form.save(commit=False)
                review.book = book
                review.upvotes = 0
                review.save()

                return redirect(reverse('rango:show_book',
                                        kwargs={'book_title_slug':
                                                book_title_slug}))

    else:
        print(form.errors)

    context_dict = {'form': form, 'book': book}
    return render(request, 'rango/leave_review.html', context=context_dict)


def contact_us(request):
    return render(request, 'rango/contact_us.html')


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


def search(request):
    context_dict = {}
    if request.method == 'POST':
        if request.method == 'POST':
            query = request.POST['query'].strip()

            if query:
                context_dict['result_list'] = run_query(query)
                context_dict['query'] = query
    return render(request, 'rango/search.html', context=context_dict)


@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)

    context_dict = {'form': form}
    return render(request, 'rango/profile_registration.html', context_dict)


class AboutView(View):
    def get(self, request):
        context_dict = {}

        visitor_cookie_handler(request)
        context_dict['visits'] = request.session['visits']

        return render(request,
                      'rango/about.html',
                      context_dict)


class AddBookView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = BookForm()
        return render(request, 'rango/add_book.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
            return render(request, 'rango/add_book.html', {'form': form})


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'picture': user_profile.picture, })

        return (user, user_profile, form)

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}

        return render(request, 'rango/profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))

        form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}

        return render(request, 'rango/profile.html', context_dict)


class ListProfilesView(View):
    @method_decorator(login_required)
    def get(self, request):
        profiles = UserProfile.objects.all()
        return render(request,
                      'rango/list_profiles.html',
                      {'user_profile_list': profiles})


@login_required
def delete_account(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user.delete()
        return redirect('/')

    return render(request, 'profile.html', {'user': user})
