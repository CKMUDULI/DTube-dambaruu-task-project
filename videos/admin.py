from django.contrib import admin

from .models import VideoPost


# Register your models here.
@admin.register(VideoPost)
class VideoPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'uploaded', 'publish_status')
    list_filter = ('uploaded', 'publish_status')
    search_fields = ('title', 'author', 'description')
    date_hierarchy = 'uploaded'
    ordering = ['publish_status', '-uploaded']
    prepopulated_fields = {'slug': ('title',)}
