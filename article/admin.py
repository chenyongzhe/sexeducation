from django.contrib import admin
from .models import Article,ArticleUserinfor,Video,Type,Message,Videolist,Vcomment,Message,IpTable,Danmu,Comment,Usermessage
admin.site.site_header = '伊甸园的烦恼后台管理'
admin.site.site_title = '伊甸园的烦恼后台管理'
admin.site.index_title="管理网站数据"

admin.site.register(Article)
admin.site.register(ArticleUserinfor)
admin.site.register(Videolist)
admin.site.register(Message)
admin.site.register(Vcomment)
admin.site.register(Comment)
admin.site.register(Danmu)
admin.site.register(Usermessage)
admin.site.register(IpTable)