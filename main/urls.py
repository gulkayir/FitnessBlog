
from django.urls import path

from main.views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('new/', SearchView.as_view(), name='new'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category'),
    path('single-article/<int:pk>/', article_detail, name='article-detail'),
    path('add-article', add_article, name='add-article'),
    path('update-article/<int:pk>/', update_article, name='update-article'),
    path('delete-article/<int:pk>/', DeleteArticleView.as_view(), name='delete-article'),
    path('user/favourits', user_favourites,name='user_favourites'),
    path('product/<int:pk>/like_or_unlike', like_or_unlike,name='like' ),

]