from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login_view", views.login_view, name="login"),
    path("logout_view", views.logout_view, name="logout"),
    path("user/<int:user_id>/", views.user_profile, name="user_profile"),
    path("show_users/", views.show_users, name="show_users"),
    path("mychats/", views.mychats, name="mychats"),
    path("chat_room/<int:chat_id>/", views.chat_room, name="chat_room"),
    path("send_message/<int:chat_id>", views.send_message, name="send_message"),
]