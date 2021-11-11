from datetime import datetime

from django import forms

from .models import Article, Image


class ArticleForm(forms.ModelForm):
    created = forms.DateTimeField(initial=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), required=False)

    class Meta:
        model = Article
        fields = '__all__'
        exclude = ('user',)

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', )
