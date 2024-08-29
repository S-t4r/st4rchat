from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Chat, Message, User

# Create your views here.
def index(request):
    return render(request, 'chat/index.html')


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
        new_chat = Chat.objects.create()
        new_chat.users.add(request.user, target_user)
        return redirect("chat_room", chat_id=new_chat.id)
    else:
        user = get_object_or_404(User, id=user_id)
        return render(request, "chat/user_profile.html", {
            "user": user,
        })



def show_users(request):
    users = User.objects.all()
    return render(request, "chat/show_users.html", {
        "users": users
    })


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

    return render(request, "chat/chat_room.html", {
        "chat": chat,
        "messages": messages,
    })



@login_required
def send_message(request, chat_id):
    content = request.POST['content']
    chat = get_object_or_404(Chat, id=chat_id)
    Message.objects.create(chat=chat, user=request.user, content=content)
    return redirect('chat_room', chat_id=chat.id)
