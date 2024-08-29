import bleach
import json

from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator

from .models import Chat, Message, Posts, User

# Create your views here.
def index(request):
    posts = Posts.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "chat/index.html", {
        "page_obj": page_obj,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "chat/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "chat/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "chat/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, karma=0)
            user.save()
        except IntegrityError:
            return render(request, "chat/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "chat/register.html")



def user_profile(request, user_id):
    if request.method == 'POST':
        target_user = get_object_or_404(User, pk=user_id)
        new_chat = Chat.objects.filter(users=target_user).filter(users=request.user).first()

        if not new_chat:
            new_chat = Chat.objects.create()
            new_chat.users.add(request.user, target_user)
        return redirect("chat_room", chat_id=new_chat.id)

    else:
        user = get_object_or_404(User, id=user_id)
        posts = user.user_posts.all().order_by("-timestamp")
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "chat/user_profile.html", {
            "user": user,
            "page_obj": page_obj,
        })



def show_users(request):
    users = User.objects.all()
    return render(request, "chat/show_users.html", {
        "users": users
    })


@login_required
def mychats(request):
    if request.method == 'POST':
        pass
    else:
        chats = Chat.objects.filter(users=request.user) | Chat.objects.filter(pk=1)
        return render(request, "chat/mychats.html", {
        "chats": chats,
    })



@login_required
def chat_room(request, chat_id=1): # Default chat_id to 1
    # Ensure the default chat exists
    if not Chat.objects.filter(pk=1).exists():
        Chat.objects.create(pk=1)
    
    chat = get_object_or_404(Chat, pk=chat_id)
    messages = Message.objects.filter(chat=chat).order_by("-timestamp")

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(chat=chat, user=request.user, content=content)
            chat.users.add(request.user) # Add user to chat temporarily

    chat_dict = model_to_dict(chat)
    chat_dict['users'] = [
    {"id": user.id, "username": user.username} for user in chat.users.all()
    ]

    return render(request, "chat/chat_room.html", {
        "chat": chat_dict,
        "messages": messages,
    })



@login_required
def send_message(request, chat_id):
    content = request.POST['content']
    chat = get_object_or_404(Chat, id=chat_id)
    Message.objects.create(chat=chat, user=request.user, content=content)
    return redirect('chat_room', chat_id=chat.id)



@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST["new_post"]

        # If content is empty
        if content == "":
            return render(request, "chat/index.html", {
                "message": "Post cannot be empty."
            })
        
        user = request.user

        # Create new post
        try:
            post = Posts.objects.create(content=content, user=user)
            post.save()
        except IntegrityError:
            return render(request, "chat/index.html", {
                "message": "Something went wrong when posting."
            })
        
        return redirect("index")


@login_required
def delete_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Posts, pk=post_id)
        post.delete()
        return JsonResponse({'success': 'Post updated successfully'}, status=200)


@login_required
def likes(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        post_id = data["post_id"]

        with transaction.atomic():
            post = Posts.objects.select_for_update().get(id=post_id)
            has_liked = post.likes.filter(id=user.id).exists()

        # If user is liking the post
        if not has_liked:
            post.likes.add(user)
        # If user is un-liking the post
        else:
            post.likes.remove(user)
        
        post.save()

        return JsonResponse({'success': 'Post updated successfully', 'new_like_count': post.likes.count()})
    


def follow(request, user_id):
    if request.method == "POST":
        target_user = get_object_or_404(User, pk=user_id)
        # Check if user is in followers
        is_follower = target_user.followers.filter(id=request.user.id).exists()

        # If hasn't yet followed
        if not is_follower:
            target_user.followers.add(request.user)
        else:
            target_user.followers.remove(request.user)
        
        return redirect("user_profile", user_id=user_id)



def following(request):
    user = get_object_or_404(User, id=request.user.id)
    following_users = user.following.all()
    following_posts = Posts.objects.filter(user__in=following_users).order_by("-timestamp")
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "chat/following.html", {
        "page_obj": page_obj
    })



def edit(request, post_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        content = data.get('content')
        if not content:
            return JsonResponse({'error': "Content must be a string"}, status=400)
        
        if not isinstance(content, str):
            return JsonResponse({'error': 'Content must be a string'}, status=400)
        
        content = bleach.clean(content)

        if len(content) > 500:
            return JsonResponse({'error': 'Content is too long'}, status=400)
        
        post = Posts.objects.get(id=post_id)
        post.content = content
        post.save()

        return JsonResponse({'success': 'Post updated successfully', 'content': post.content}, status=200)