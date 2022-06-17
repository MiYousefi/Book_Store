from django.contrib import admin

from .models import Book, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['book', 'user','is_active', 'recommend', 'datetime_created']


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price']


admin.site.register(Book, BookAdmin)
