from django.db import models

from account.models import User
class Category(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50)
    name = models.CharField(max_length=55)
    image = models.ImageField(blank=True, null=True, upload_to='categories')
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.parent:
            return f'{self.name} --> {self.parent}'
        return self.name

    @property
    def get_children(self):
        if self.children:
            return self.children.all()
        return False

class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    cooking_time = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    created = models.DateTimeField()

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='articles', blank=True)
    recipe = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        if self.image:
            return self.image.url
        return ''
