from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Tags, Feedback, InfoAboutRock


class PostAdmin(SummernoteModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('author', 'title', 'text', 'thumb', 'tags', 'created_date', 'published_date')
        }),
        ('Дополнительные опции для пород и минералов', {
            'classes': ('collapse',),
            'fields': ('Infobox',),
        }),
    )
    summernote_fields = ('text')
    list_display = ("title", "get_products", "published_date")
    search_fields = ("text", "title")
    list_filter = ("tags", "published_date")

    def get_products(self, obj):
        return "\n".join([p.name for p in obj.tags.all()])


class infoboxAdmin(SummernoteModelAdmin):
    summernote_fields = ('formula')


admin.site.register(Post, PostAdmin)
admin.site.register(Tags)
admin.site.register(InfoAboutRock, infoboxAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("comment", "title", "email", "created")
    list_filter = ("created", "title")
    search_fields = ("comment", "title")
    readonly_fields = ("comment", "title")
    ordering = ("-created",)


admin.site.register(Feedback, FeedbackAdmin)
