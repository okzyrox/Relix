from django.urls import path, include
from . import views

urlpatterns = [
    path("server/players/", views.serverPlayersList, name="currentPlayerCounts"),
    path("server/listings/", views.serverList, name='publicServers')
]