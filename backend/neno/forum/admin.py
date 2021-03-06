from neno.forum.models import *
from django.contrib import admin

class PostInline(admin.StackedInline):
    model = Post
    extra = 1

class DiscussionAdmin(admin.ModelAdmin):
    list_filter = ['created']
    search_fields = ['subject']
    date_hierarchy = 'created'
    inlines = [PostInline]
    list_display = ['id', 'subject', 'slug', 'created']

class PostAdmin(admin.ModelAdmin):
    list_filter = ['created', 'author']
    search_fields = ['subject', 'original_body', 'author']
    date_hierarchy = 'created'
    list_display = ['id', 'subject', 'author', 'hits', 'created', 'discussion']

class ProfileAdmin(admin.ModelAdmin):
    list_filter = ['created', 'last_online', 'birth_date', 'gender']
    search_fields = ['name', 'email', 'original_body', 'author', 'homepage', 'registration_ip']
    date_hierarchy = 'created'
    list_display = ['id', 'name', 'email', 'gender', 'registration_ip', 'last_online', 'created']

class EmoteAdmin(admin.ModelAdmin):
    list_filter = ['created']
    date_hierarchy = 'created'
    list_display = ['id', 'image_html', 'name', 'code', 'created']

class IconAdmin(admin.ModelAdmin):
    list_filter = ['created']
    date_hierarchy = 'created'
    list_display = ['id', 'image_html', 'name', 'created']

admin.site.register(Post, PostAdmin)
admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Emote, EmoteAdmin)
admin.site.register(Icon, IconAdmin)
