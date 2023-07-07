from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("server/players/", views.serverPlayersList, name="currentPlayerCounts"),
    path("server/listings/", views.serverList, name='publicServers'),
    path("login/", csrf_exempt(views.login),name='authUser'),
    path("logout/", views.logout, name="deauthUser"),
    path("newuser/", views.createUser, name="newHelixUser"),
    path("userexists/", views.userExistsView, name="checkExistance"),
]