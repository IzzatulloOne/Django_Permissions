from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Genre, Movie, Comment, Author

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')
    list_display_links = ('id', 'type')
    search_fields = ('type',)
    ordering = ('type',)

    fields = ('type',)

class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'director', 'genre', 'author', 'release', 'published', 'get_image')
    list_display_links = ('id', 'title', 'get_image')
    search_fields = ('title', 'description', 'author__user__username')  # можно искать по имени пользователя
    list_filter = ('genre', 'release', 'author')  # фильтр по автору
    list_editable = ('director', 'genre', 'published')
    inlines = [CommentInline]

    def get_image(self, obj: Movie):
        if obj.cover:
            return mark_safe(f"<img src='{obj.cover.url}' width='60px' />")
        return "No Image"
    get_image.short_description = "Cover"

    fieldsets = (
        ("Ma'lumotlar", {
            'fields': ('title', 'director', 'description', 'genre', 'author'),
        }),
        ("Media fayllar", {
            'fields': ('cover', 'video')
        }),
        ("Qo‘shimcha", {
            'fields': ('release', 'published')
        }),
    )

admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'job')
    list_display_links = ('id', 'user')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('job',)
    ordering = ('user__username',)
    fields = ('user', 'photo', 'phone', 'job', 'website', 'address', 'bio', 'twitter', 'facebook', 'telegram', 'linkedin')

admin.site.register(Author, AuthorAdmin)