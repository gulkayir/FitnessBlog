from datetime import datetime

from django import forms
from django.db import models
from django.db.models import fields

from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    created = forms.DateTimeField(initial=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), required=False)

    class Meta:
        model = Article
        fields = '__all__'
        exclude = ('user',)


<<<<<<< HEAD
class SearchForm(forms.Form):
    query = forms.CharField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email','content')
=======
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
>>>>>>> ed8a8747dde4ec6fc09406bf6a96e5408cc780a8
