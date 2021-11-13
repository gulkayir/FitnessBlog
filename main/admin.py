from django.contrib import admin

from main.models import *

class ImageInlineAdmin(admin.TabularInline):
    model = Image
    fields = ('image',)
    max_num = 5

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ImageInlineAdmin,]

admin.site.register(Category)


admin.site.register(Comment)