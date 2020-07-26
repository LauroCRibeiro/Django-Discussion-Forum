from django.contrib import admin
from .models import ForumThread,ThreadReply,Setting
# Register your models here.
class ForumThreadModelAdmin(admin.ModelAdmin):
    list_display=('title','tags')
admin.site.register(ForumThread,ForumThreadModelAdmin)

class ThreadReplyModelAdmin(admin.ModelAdmin):
    list_display=('title','thread_id')
admin.site.register(ThreadReply,ThreadReplyModelAdmin)

class SettingAdmin(admin.ModelAdmin):
    list_display=('user_id','signature')
admin.site.register(Setting,SettingAdmin)

