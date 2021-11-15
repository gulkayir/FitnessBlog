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
    likes = models.ManyToManyField(User)



    def __str__(self):
        return self.title

<<<<<<< HEAD

=======
    def get_absolute_url(self):
        return reverse('article-detail', kwargs={
            'pk':self.pk
        })
    
>>>>>>> ed8a8747dde4ec6fc09406bf6a96e5408cc780a8
    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')




class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    #name = models.CharField(max_length=80)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #email = models.EmailField()
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

<<<<<<< HEAD
class Comment(models.Model):
    name = models.CharField(max_lenght=50)
    email = models.EmailField(max_lenght=100)
    content = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f'Comment by {self.name}'







=======
    def __str__(self):
        return 'Comment {} by {}'.format(self.content, self.author)
>>>>>>> ed8a8747dde4ec6fc09406bf6a96e5408cc780a8
