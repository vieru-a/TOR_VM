from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name')
    list_display_links = ('id', 'email')
    search_fields = ('email', 'first_name', 'last_name')
