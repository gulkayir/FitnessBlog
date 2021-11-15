
from django.urls import path

from main.views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category'),
    path('single-article/<int:pk>/', article_detail, name='article-detail'),
    path('add-article', add_article, name='add-article'),
    path('update-article/<int:pk>/', update_article, name='update-article'),
    path('delete-article/<int:pk>/', DeleteArticleView.as_view(), name='delete-article'),
<<<<<<< HEAD
    # path('search', SearchListView.as_view(), name='search'),

=======
>>>>>>> ed8a8747dde4ec6fc09406bf6a96e5408cc780a8
]