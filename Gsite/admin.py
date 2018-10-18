from django.contrib import admin
from .models import Post, Tags, Feedback
from django_summernote.admin import SummernoteModelAdmin

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('text',)

admin.site.register(Post, PostAdmin)
admin.site.register(Tags)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("comment", "title",   "email", "created")
    list_filter = ("created",  "title")
    search_fields = ("comment", "title")
    readonly_fields = ("comment", "title")
    ordering = ("-created",)

admin.site.register(Feedback, FeedbackAdmin)