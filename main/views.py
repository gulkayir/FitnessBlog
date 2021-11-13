from datetime import timedelta

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

from .forms import ArticleForm, CommentForm, ImageForm
from .models import *
# from .permissions import UserHasPermissionMixin


# def index(request):
#     recipes = Recipe.objects.all()
#     return render(request, 'index.html', locals())

# def category_detail(request, slug):
#     category = Category.objects.get(slug=slug)
#     recipes = Recipe.objects.filter(category_id=slug)
#     return render(request, 'category-detail.html', locals())

# def recipe_detail(request, pk):
#     recipe = get_object_or_404(Recipe, pk=pk)
#     image = recipe.get_image
#     images = recipe.images.exclude(id=image.id)
#     return render(request, 'recipe-detail.html', locals())

# def recipe_detail(request, pk):
#     recipe = get_object_or_404(Recipe, pk=pk)
#     image = recipe.get_image
#     images = recipe.images.exclude(id=image.id)
#     return render(request, 'recipe-detail.html', locals())

# def delete_recipe(request, pk):
#     recipe = get_object_or_404(Recipe, pk=pk)
#     if request.method == 'POST':
#         recipe.delete()
#         messages.add_message(request, messages.SUCCESS, 'Successfully deleted recipe')
#         return redirect('home')
#     return render(request, 'delete-recipe.html')

# class ArticleDetailView(DetailView):
#     model = Article
#     template_name = 'single-article.html'
#     context_object_name = 'article'


class MainPageView(ListView):
    model = Article
    template_name = 'home.html'
    context_object_name = 'articles'
    paginate_by = 2



    def get_template_names(self):
        template_name = super(MainPageView, self).get_template_names()
        search = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        if search:
            template_name = 'search.html'
        elif filter:
            template_name = 'filtered.html'
        return template_name

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        search = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        if search:
            context['articles'] = Article.objects.filter(Q(title__icontains=search)|Q(description__icontains=search))
        elif filter:
            start_data = timezone.now() - timedelta(days=1)
            context['articles'] = Article.objects.filter(created__gte=start_data)
        else:
            context['article'] = Article.objects.all()
        context['categories'] = Category.objects.filter(parent__isnull=True)
        context['comment'] = Comment.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category-detail.html'
    context_object_name = 'category'

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
    image = article.get_image
    images = article.images.exclude(id=image.id)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
        else:
            comment_form = CommentForm()
    return render(request, 'single-article.html', locals())

@login_required(login_url='login')
def add_article(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if article_form.is_valid() and formset.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()

            for form in formset.cleaned_data:
                image = form['image']
                Image.objects.create(image=image, article=article)
            return redirect(article.get_absolute_url())
    else:
        article_form = ArticleForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'add-article.html', locals())

def update_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user == article.user:
        ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
        article_form = ArticleForm(request.POST or None, instance=article)
        formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.filter(article=article))
        if article_form.is_valid() and formset.is_valid():
            article = article_form.save()
            for form in formset:
                image = form.save(commit=False)
                image.recipe = article
                image.save()
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

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'single-post.html'

    def form_valid(self, form):
        form.instance.article_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('article-detail')