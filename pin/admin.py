from django.contrib import admin

from pin.models import Post, Notify

class PinAdmin(admin.ModelAdmin):
    list_display = ('id', 'text','user','admin_image' )
    
class NotifyAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'user', 'text', 'seen', 'type')
    list_filter = ('seen',)

admin.site.register(Post, PinAdmin)
admin.site.register(Notify, NotifyAdmin)

