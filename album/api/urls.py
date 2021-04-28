from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('music_add', CreateMusicAPIView.as_view(), name='music_add'),
    path('music_list', MusicListView.as_view(), name='music_list'),
    path('ratings_add', CreateRatingsAPIView.as_view(), name='ratings_add'),
]
