from django.contrib import admin
from .models import *


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('replyAd', 'replyUser', 'dateCreation', 'text', 'status_remove', 'status_add')
    list_filter = ('status_remove', 'status_add', 'dateCreation')
    search_fields = ('replyUser', 'text')


admin.site.register(Reply, ReplyAdmin)
admin.site.register(Advertisement)
