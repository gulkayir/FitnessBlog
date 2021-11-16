from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.expressions import F
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse, request
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.utils import timezone
from django.utils.translation import templatize
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import ArticleForm, CommentForm
from .models import *


class MainPageView(ListView):
    model = Article
    template_name = 'home.html'
    context_object_name = 'articles'
    paginate_by = 2



    def get_template_names(self):
        template_name = super(MainPageView, self).get_template_names()
        search = self.request.GET.get('q')
        if search:
            template_name = 'search.html'

        return template_name

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        search = self.request.GET.get('q')
        if search:
            context['articles'] = Article.objects.filter(Q(title__icontains=search)|Q(description__icontains=search))
        else:
            context['article'] = Article.objects.all()
        context['categories'] = Category.objects.filter(parent__isnull=True)
        context['comment'] = Comment.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category-detail.html'
    context_object_name = 'category'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.slug = kwargs.get('slug', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(category_id=self.slug)
        return context


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    template_name = 'single-article.html'
    comments = article.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        comment_form.author = request.user
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.author = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, template_name,  {'article': article,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


@login_required(login_url='login')
def add_article(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        if article_form.is_valid() :
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect(article.get_absolute_url())
    else:
        article_form = ArticleForm()
    return render(request, 'add-article.html', locals())

def update_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user == article.user:
        article_form = ArticleForm(request.POST or None, instance=article)
        if article_form.is_valid():
            article = article_form.save()
            
            return redirect(article.get_absolute_url())
        return render(request, 'update-article.html', locals())
    else:
        return HttpResponse('<h1>403 Forbidden</h1>')


class DeleteArticleView( DeleteView):
    model = Article
    template_name = 'delete-article.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.add_message(request, messages.SUCCESS, 'Successfully deleted recipe')

        return HttpResponseRedirect(success_url)


def like_or_unlike(request,pk):
    article = Article.objects.get(pk=pk)
    if request.user in article.likes.all():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return redirect(article.get_absolute_url())


def user_favourites(request):
    user_favourites = Article.objects.filter(likes=request.user)
    paginator = Paginator(user_favourites, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'favorites.html', locals())


class SearchView(ListView):
    model = Article
    template_name = 'new.html'
    context_object_name = 'articles'
    paginate_by = 4


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        time_threshold = datetime.now(timezone.utc) - timedelta(hours=1)
        context['articles'] = Article.objects.filter(created__lte=time_threshold)
        return context


