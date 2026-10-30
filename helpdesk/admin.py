from django.contrib import admin

from .models import ChatFeedback


@admin.register(ChatFeedback)
class ChatFeedbackAdmin(admin.ModelAdmin):
    list_display = ("question", "is_helpful", "created_at")
    list_filter = ("is_helpful", "created_at")
    search_fields = ("question",)
    readonly_fields = ("created_at",)
