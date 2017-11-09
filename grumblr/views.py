from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.tokens import default_token_generator

# Django transaction system so we can use @transaction.atomic
from django.db import transaction
from django.template.loader import render_to_string

from django.http import Http404, HttpResponse
# Imports the Item class
from grumblr.models import *

# import time
import datetime

# import forms
from grumblr.forms import Registration, PostForm, EditProfile, ChangePassword, \
                          Comment_Form

# used to send email with Django
from django.core.mail import send_mail

from django.views.decorators.csrf import ensure_csrf_cookie


# Create your views here.
@login_required
@ensure_csrf_cookie  # Gives CSRF token for later requests.
def home(request):
    context = {}

    #delete a user
    # delete_user = User.objects.get(username='larry6').delete()
    # Profile.objects.filter(user=delete_user).delete()
    # delete_user.delete()

    # delete all
    # User.objects.all().delete()
    # Post.objects.all().delete()
    # Profile.objects.all().delete()
    context["fullName"] = "%s %s" % (request.user.first_name, 
                                    request.user.last_name)
    # context['posts'] = Post.objects.all().order_by('-date')
    context['form'] = PostForm()
    context['user1'] = request.user
    context["follower_num"] = request.user.profile.followed.count()
    context["following_num"] = request.user.profile.following.count()
    context["comments"] = []
    return render(request, 'grumblr/global_page.html', context)

@login_required
def post1(request):
    try:
        user = request.user
    except ObjectDoesNotExist:
        return Http404
    context = {}
    context["fullName"] = "%s %s" % (request.user.first_name, 
                                    request.user.last_name)

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = PostForm()
        return render(request, 'grumblr/global_page.html', context)

    # Create form for post method
    form = PostForm(request.POST)
    context['form'] = form

    if form.is_valid():
        new_post = Post(content = form.cleaned_data['content'],
                        user = request.user, 
                        date = datetime.datetime.now())
        new_post.save()
    return HttpResponse("")

    # if not content:
    #     errors.append("Post cannot be empty1.")
    # elif len(content) == 0:
    #     errors.append("Posts cannot be empty2.")
    # elif len(content) > 42:
    #     errors.append("Posts cannot be longer than 42 charactors.")
    # if errors:
    #     context["errors"] = errors
    #     context['posts'] = Post.objects.all().order_by('-date')
    #     return render(request, 'grumblr/global_page.html', context)
    # else:
    #     now = datetime.datetime.now()
    # #     new_post = Post(content = form.cleaned_data['content'], user = request.user, 
    # #                     date = datetime.datetime.now())
    # #     new_post.save()
    #     return redirect("/grumblrglobal")

@login_required
def profile1(request, id):
    context = {}
    try:
        user = User.objects.get(id = id)
        if user == request.user:
            return redirect("my_profile")
        context['posts'] = Post.objects.filter(user = user\
                            ).filter(deleted=False).order_by('-date')
        context["fullName"] = "%s %s" % (user.first_name, user.last_name)
        context['user'] = user
        context['bio'] = user.profile.bio
        # print(user.profile.bio)
        context['age'] = user.profile.age
        context['user1'] = request.user
        context['followed'] = user.profile in request.user.profile.following.all()
        context['isme'] = False
        context['intro'] = get_intro(request, user)
        return render(request, 'grumblr/profile_page.html', context)
    except ObjectDoesNotExist:
        return redirect("global")

def get_intro(request, user):
    post_num = Post.objects.filter(user=user).filter(deleted=False).count()
    follower_num = user.profile.followed.count()
    following_num = user.profile.following.count()
    ans = "%d years old, %d posts, %d followers, %d following" % (user.profile.age,
                    post_num, follower_num, following_num)
    return ans
@login_required
def my_profile(request):
    context = {}
    try:
        user = request.user
        profile = Profile.objects.get(user=user)
        context['posts'] = Post.objects.filter(user = user\
                            ).filter(deleted=False).order_by('-date')
        context["fullName"] = "%s %s" % (user.first_name, user.last_name)
        context['bio'] = user.profile.bio
        context['age'] = user.profile.age
        context['email'] = user.email
        context['user'] = user
        context['isme'] = True
        context['followed'] = True
        context['intro'] = get_intro(request, user)
        return render(request, 'grumblr/profile_page.html', context)
    except ObjectDoesNotExist:
        return render(request, 'grumblr/profile_page.html', context)

@login_required
def get_profile_stream(request, id, time="1970-01-01T00:00+00:00"):
    try:
        self_user = request.user
        user = User.objects.get(id=id)
    except ObjectDoesNotExist:
        return Http404
    max_time = Post.get_max_time()
    posts = Post.objects.filter(user = user\
                                ).filter(deleted=False).order_by('-date')
    isme = True if user==self_user else False
    for post in posts:
        post_comment_id = "post_comment_%d" % post.id
        comment_list_id = "comments_%d" % post.id
        comment_form = Comment()
        comment_btn = "comment_btn_%d" % post.id
        # post.show_comment = False
        # post.save()
        post.html = render_to_string("grumblr/post_page.html",\
                                {"post":post, "comment_id": post_comment_id,
                                "comment_form": comment_form,
                                "comment_list_id": comment_list_id,
                                "comment_btn": comment_btn,
                                "isme": isme},
                                request = request)
    context = {"max_time":max_time, "posts":posts}
    # print("get posts done.")
    return render(request, 'grumblr/posts.json', context, 
        content_type='application/json')    



@login_required
def following_stream(request):
    context = {}
    user = request.user
    context['user1'] = user
    context['intro'] = get_intro(request, user)

    context["fullName"] = "%s %s" % (user.first_name, user.last_name)
    return render(request, 'grumblr/following_page.html', context)

@login_required
def do_follow(request, id):
    try:
        user_self = request.user
        other = User.objects.get(id = id)
        # url = request.get_full_path()
        url = request.META['HTTP_REFERER']
        # url = 'profile/%s/' % id
        # print(request.META['HTTP_REFERER'])
    except ObjectDoesNotExist:
        return redirect('global')
    if other.profile in user_self.profile.following.all():
        user_self.profile.following.remove(other.profile)
    else: 
        user_self.profile.following.add(other.profile)
    user_self.profile.save()
    try:  
        return redirect(url)
    except:
        return redirect('my_profile')

@login_required
def edit_profile(request):
    # if request.method == 'POST':
    #     form = UploadFileForm(request.POST, request.FILES)
    # if form.is_valid():
    #     handle_uploaded_file(request.FILES['file'])
    #     return HttpResponseRedirect('/success/url/')
    # else:
    #     form = UploadFileForm()
    # return render(request, 'upload.html', {'form': form})
    context = {}
    try:
        user = request.user
    except ObjectDoesNotExist:
        return render(request, 'grumblr/profile_page.html', context)
    try:
        profile = Profile.objects.get(user = user)
        context["fullName"] = "%s %s" % (user.first_name, user.last_name)
    except:
        profile = Profile(user = user)
    if request.method =="GET":
        intitial_value = {'first_name': user.first_name, 
                          "last_name": user.last_name,
                          "bio": user.profile.bio,
                          "age": user.profile.age}
        context['form'] = EditProfile(initial= intitial_value)
        return render(request, 'grumblr/edit_profile.html', context)

    form = EditProfile(request.POST, request.FILES)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'grumblr/edit_profile.html', context)
    # for key in form.cleaned_data:
    #     profile.key = form.cleaned_data[key]
    # for key in form.cleaned_data:
    #     user.key = form.cleaned_data[key]
    if form.cleaned_data['image'] != None:
        profile.image = form.cleaned_data['image']
    profile.age = form.cleaned_data['age']
    profile.bio = form.cleaned_data['bio']
    user.first_name = form.cleaned_data['first_name']
    user.last_name = form.cleaned_data['last_name']
    profile.save()
    user.save()
    context['message'] = "Your profile have been modified successfully. "
    return render(request, 'grumblr/edit_profile.html', context)

@transaction.atomic
def registration(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = Registration()
        return render(request, 'grumblr/registration_page.html', context)

    # Create form for post method
    form = Registration(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'grumblr/registration_page.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'])
    new_profile = Profile(user = new_user)
    new_user.save()
    new_profile.save()

#     # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    

    # print(1)
    token = default_token_generator.make_token(new_user)
    email_body = """
    Welcome to the grumblr. Please click the link below to verify your email address:
    http://%s%s
    """%(request.get_host(),
         reverse('confirmation', args=(new_user.id, token)))
    send_mail(subject="Verify your email address.Grumblr",
            message = email_body,
            from_email="larry.l1@hotmail.com",
            recipient_list=[new_user.email])
    # print(2)
    return redirect('global')

@transaction.atomic
@login_required
def confirm_registration(request, id, token):
    # check user and token
    try:
        # print(id)
        # print(token)
        user = User.objects.get(id=id)

    except ObjectDoesNotExist:
        # print('user does not exist.')
        raise Http404

    # if not default_token_generator.check_token(user, token):
    #     print('dont match')
    #     raise Http404

    user.profile.confirmed = True
    print(user.profile.confirmed)
    user.save()
    user.profile.save()
    # profile.save()
    login(request, user)
    info = "Your registration has been confirmed. Please feel free to explore Grumblr"
    return render(request, "grumblr/send_email.html", {"info":info})

@login_required
def send_change_email(request):
    token = default_token_generator.make_token(request.user)
    email_body = """
    Please click the link below to change your password:
    http://%s%s
    """%(request.get_host(),
         reverse('change_password', args=(request.user.username, token)))
    send_mail(subject="Change your password.Grumblr",
            message = email_body,
            from_email="larry.l1@andrew.cmu.edu",
            recipient_list=[request.user.email])
    info = "Email has been sent. Please login your email to change your password"
    return render(request, "grumblr/send_email.html", {"info":info})

@login_required
def send_confirm_email(request):
    token = default_token_generator.make_token(request.user)
    email_body = """
    Welcome to the grumblr. Please click the link below to verify your email address:
    http://%s%s
    """%(request.get_host(),
         reverse('confirmation', args=(request.user.id, token)))
    send_mail(subject="Verify your email address.Grumblr",
            message = email_body,
            from_email="larry.l1@andrew.cmu.edu",
            recipient_list=[request.user.email])
    return redirect('global')

@transaction.atomic
def change_password(request, username, token):
    context = {}
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        # print('user does not exist.')
        raise Http404

    if not default_token_generator.check_token(user, token):
        print('dont match')
        raise Http404

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = ChangePassword()
        return render(request, 'grumblr/change_password.html', context)

    # Create form for post method
    form = ChangePassword(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'grumblr/change_password.html', context)
    user.set_password(form.cleaned_data['password1'])  
    user.save()
    info = "Your password has been changed."
    login(request, user)
    return render(request, "grumblr/send_email.html", {"info":info})

# @login_required
# def do_search(request):
#     context = {}
#     email = request.POST.get('email', "not there")
#     if email.contains('@'):
#         try:
#             user = User.objects.get(email = email)
#             if user == request.user:
#                 return redirect("/my_profile")
#             context['posts'] = Post.objects.filter(user = user).order_by('-date')
#             context["fullName"] = "%s %s" % (user.first_name, user.last_name)
#             context['user'] = user
#             context['bio'] = user.profile.bio
#             print(user.profile.bio)
#             context['age'] = user.profile.age
#             context['user1'] = request.user
#             context['followed'] = user.profile in request.user.profile.following.all()
#             context['isme'] = False
#             context['intro'] = get_intro(request, user)
#             return render(request, 'grumblr/profile_page.html', context)
#         except ObjectDoesNotExist:
#             return render(request, "grumblr/send_email.html",
#                         {"info": "Grumblr does not exists."})

@login_required
def delete_post(request, id):
    try: 
        post = Post.objects.get(id = id)
        user = request.user
    except ObjectDoesNotExist:
        return redirect("global")

    if (post.user == user):
        post.deleted = True
        post.save()

    return redirect('my_profile')



@login_required
def get_changes(request, time="1970-01-01T00:00+00:00"):
    max_time = Post.get_max_time()
    # print(time)
    posts = Post.get_changes(time)
    for post in posts:
        comment_form = Comment()
        comment_btn = "comment_btn_%d" % post.id
        post_comment_id = "post_comment_%d" % post.id
        comment_list_id = "comments_%d" % post.id
        post.html = render_to_string("grumblr/post_page.html",\
                                {"post":post, "comment_id": post_comment_id,
                                "comment_form": comment_form,
                                "comment_list_id": comment_list_id,
                                "comment_btn": comment_btn},
                                request = request)

    context = {"max_time":max_time, "posts":posts}
    return render(request, 'grumblr/posts.json', context, 
            content_type='application/json')

# Returns all recent additions in the database, as JSON
@login_required
def get_posts(request, time="1970-01-01T00:00+00:00"):
    max_time = Post.get_max_time()
    posts = Post.get_posts(time)
    for post in posts:
        post_comment_id = "post_comment_%d" % post.id
        comment_list_id = "comments_%d" % post.id
        comment_form = Comment()
        comment_btn = "comment_btn_%d" % post.id
        # post.show_comment = False
        # post.save()
        post.html = render_to_string("grumblr/post_page.html",\
                                {"post":post, "comment_id": post_comment_id,
                                "comment_form": comment_form,
                                "comment_list_id": comment_list_id,
                                "comment_btn": comment_btn},
                                request = request)
    context = {"max_time":max_time, "posts":posts}
    # print("get posts done.")
    return render(request, 'grumblr/posts.json', context, 
        content_type='application/json')


@login_required
def add_comment(request, id):
    try:
        post = Post.objects.get(id=id)
        user = request.user
    except ObjectDoesNotExist:
        return HttpResponse("The post you want to comment does not exist.")

    form = Comment_Form(request.POST)

    if not form.is_valid():
        return HttpResponse("Form not valid.")

    new_comment = Comment(content = form.cleaned_data['content'],
                    profile = request.user.profile, 
                    post = post,
                    time = datetime.datetime.now())
    new_comment.save()

    new_comment.html = render_to_string("grumblr/comment.html", {"post":post,
                        "comment": new_comment, "user": user})
    return render(request, 'grumblr/comment.json', {"comment":new_comment}, 
        content_type='application/json')

@login_required
def get_comment(request, id, time="1970-01-01T00:00+00:00"):
    try:
        post = Post.objects.get(id = id)
        user = request.user
    except ObjectDoesNotExist:
        return HttpResponse("The post you want to comment does not exist.")

    max_time = Comment.get_max_time()
    comments = Comment.get_comments(post, time)
    for comment in comments:
        comment.html = render_to_string("grumblr/comment.html", 
                                        {"comment":comment, "user": user})
    context = {"max_time":max_time, "comments":comments, "post_id": post.id}
    # print("get posts done.")
    return render(request, 'grumblr/comments.json', context, 
        content_type='application/json')

@login_required
def get_following(request, time="1970-01-01T00:00+00:00"):
    max_time = Post.get_max_time()
    try:
        user = request.user
    except ObjectDoesNotExist:
        return Http404
    followees = user.profile.following.all()
    following_user = []
    for followee in followees:
        followee_user = followee.get_user()
        following_user.append(followee_user)
    posts = Post.objects.filter(user__in=following_user\
                                ).filter(deleted=False).order_by('-date')
    for post in posts:
        post_comment_id = "post_comment_%d" % post.id
        comment_list_id = "comments_%d" % post.id
        comment_form = Comment()
        comment_btn = "comment_btn_%d" % post.id
        # post.show_comment = False
        # post.save()
        post.html = render_to_string("grumblr/post_page.html",\
                                {"post":post, "comment_id": post_comment_id,
                                "comment_form": comment_form,
                                "comment_list_id": comment_list_id,
                                "comment_btn": comment_btn},
                                request = request)
    context = {"max_time":max_time, "posts":posts}
    # print("get posts done.")
    return render(request, 'grumblr/posts.json', context, 
        content_type='application/json')

