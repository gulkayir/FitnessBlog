from django.db import models
from django.db.models.fields.related import ForeignKey
from django.urls import reverse

from account.models import User

class Category(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50)
    name = models.CharField(max_length=55)
    image = models.ImageField(blank=True, null=True, upload_to='categories')
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.parent:
            return f'{self.parent}/{self.name}'
        return self.name

    @property
    def get_children(self):
        if self.children:
            return self.children.all()
        return False

class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(blank=True, upload_to='images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    created = models.DateTimeField()
    likes = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={
            'pk':self.pk
        })
    
    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')




class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.content, self.author)
