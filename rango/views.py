from django.shortcuts import render
#from django.http import HttpResponse
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
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    book_list = Book.objects.all()
    review_list = Review.objects.order_by('-upvotes')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'What book are you going to read today?'
    context_dict['books'] = book_list
    context_dict['reviews'] = review_list

    # Call the helper function to handle the cookies
    # visitor_cookie_handler(request)
    response = render(request, 'rango/index.html', context=context_dict)

    # Return response back to the user, updating any cookies that need changed.
    return response


def about(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/about.html', context=context_dict)
    return response


def show_book(request, book_title_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        book = Book.objects.get(slug=book_title_slug)
        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list.
        reviews = Review.objects.filter(book=book)
        # Adds our results list to the template context under name pages.
        context_dict['reviews'] = reviews
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['book'] = book
    except Book.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['book'] = None
        context_dict['reviews'] = None

    # Go render the response and return it to the client.
    return render(request, 'rango/book.html', context=context_dict)


@login_required
def add_book(request):
    form = BookForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = BookForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/rango/')

        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_book.html', {'form': form})


@login_required
def leave_review(request, book_title_slug):
    try:
        book = Book.objects.get(slug=book_title_slug)
    except Book.DoesNotExist:
        book = None

    # You cannot add a page to a Category that does not exist...
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

# def register(request):
#     # A boolean value for telling the template
#     # whether the registration was successful.
#     # Set to False initially. Code changes value to
#     # True when registration succeeds.
#     registered = False

#     # If it's a HTTP POST, we're interested in processing form data.
#     if request.method == 'POST':
#         # Attempt to grab information from the raw form information.
#         # Note that we make use of both UserForm and UserProfileForm.
#         user_form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST)

#         # If the two forms are valid...
#         if user_form.is_valid() and profile_form.is_valid():
#             # Save the user's form data to the database.
#             user = user_form.save()

#             # Now we hash the password with the set_password method.
#             # Once hashed, we can update the user object.
#             user.set_password(user.password)
#             user.save()

#             # Now sort out the UserProfile instance.
#             # Since we need to set the user attribute ourselves,
#             # we set commit=False. This delays saving the model
#             # until we're ready to avoid integrity problems.
#             profile = profile_form.save(commit=False)
#             profile.user = user

#             # Did the user provide a profile picture?
#             # If so, we need to get it from the input form and
#             # put it in the UserProfile model.
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']

#             # Now we save the UserProfile model instance.
#             profile.save()

#             # Update our variable to indicate that the template
#             # registration was successful.
#             registered = True

#         else:
#             # Invalid form or forms - mistakes or something else?
#             # Print problems to the terminal.
#             print(user_form.errors, profile_form.errors)

#     else:
#         # Not a HTTP POST, so we render our form using two ModelForm instances.
#         # These forms will be blank, ready for user input.
#         user_form = UserForm()
#         profile_form = UserProfileForm()

#     # Render the template depending on the context.
#     return render(request,
#                 'rango/register.html',
#                 context = {'user_form': user_form,
#                             'profile_form': profile_form,
#                             'registered': registered})

# def user_login(request):
#     # If the request is a HTTP POST, try to pull out the relevant information.
#     if request.method == 'POST':
#         # Gather the username and password provided by the user.
#         # This information is obtained from the login form.
#         # We use request.POST.get('<variable>') as opposed
#         # to request.POST['<variable>'], because the
#         # request.POST.get('<variable>') returns None if the
#         # value does not exist, while request.POST['<variable>']
#         # will raise a KeyError exception.
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         # Use Django's machinery to attempt to see if the username/password
#         # combination is valid - a User object is returned if it is.
#         user = authenticate(username=username, password=password)

#         # If we have a User object, the details are correct.
#         # If None (Python's way of representing the absence of a value), no user
#         # with matching credentials was found.
#         if user:
#             # Is the account active? It could have been disabled.
#             if user.is_active:
#             # If the account is valid and active, we can log the user in.
#             # We'll send the user back to the homepage.
#                 login(request, user)
#                 return redirect(reverse('rango:index'))
#             else:
#                 # An inactive account was used - no logging in!
#                 return HttpResponse("Your Rango account is disabled.")
#         else:
#             # Bad login details were provided. So we can't log the user in.
#             print(f"Invalid login details: {username}, {password}")
#             return HttpResponse("Invalid login details supplied.")

#         # The request is not a HTTP POST, so display the login form.
#         # This scenario would most likely be a HTTP GET.
#     else:
#         # No context variables to pass to the template system, hence the
#         # blank dictionary object...
#         return render(request, 'rango/login.html')


def contact_us(request):
    return render(request, 'rango/contact_us.html')

# # Use the login_required() decorator to ensure only those logged in can
# # access the view.
# @login_required
# def user_logout(request):
#     # Since we know the user is logged in, we can now just log them out.
#     logout(request)
#     # Take the user back to the homepage.
#     return redirect(reverse('rango:index'))

# A helper method


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# Updated the function definition


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
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
        form = UserProfileForm({'picture': user_profile.picture,})
        
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
        
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

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