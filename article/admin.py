from django.contrib import admin
from .models import Article,ArticleUserinfor,Video,Type,Message
# Register your models here.
admin.site.register(Article)
admin.site.register(ArticleUserinfor)
admin.site.register(Video)
admin.site.register(Type)
admin.site.register(Message)