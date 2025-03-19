from django.contrib import admin
from movies.models import Genre, Movie, Person, Contact, Video, Comment  # Slider kaldırıldı

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('name', 'email', 'text', 'rating', 'created_date')
    can_delete = False

class MovieAdmin(admin.ModelAdmin):
    list_display=('title','is_active','is_home')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('genres','language', 'is_active', 'is_home')
    search_fields = ('title', 'description')
    inlines = [CommentInline]

class PersonAdmin(admin.ModelAdmin):
    list_display=('full_name', 'gender', 'duty_type')
    list_filter = ('gender', 'duty_type')
    search_fields = ('first_name', 'last_name')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'movie', 'created_date', 'active')
    list_filter = ('active', 'created_date')
    search_fields = ('name', 'email', 'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre)
admin.site.register(Person, PersonAdmin)
admin.site.register(Contact)
admin.site.register(Video)
admin.site.register(Comment, CommentAdmin)
