# -*- coding: utf-8 -*-
import time

from django.contrib import admin

from pin.models import Post, Category, App_data, Comments, send_notif, Notif
from user_profile.models import Profile


class PinAdmin(admin.ModelAdmin):
    list_filter = ('status', 'report', 'is_ads', 'show_in_default', 'category')
    search_fields = ['id', 'user__id']

    list_display = ('id', 'text', 'get_user_url', 'category', 'admin_image',
                    'status', 'like', 'device', 'is_ads',
                    'show_in_default', 'report')

    actions = ['make_approve',
               'make_approve_go_default',
               'really_delete_selected',
               'delete_all_user_posts',
               'fault',
               'no_problem']

    def get_actions(self, request):
        actions = super(PinAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def make_approve(self, request, queryset):
        for obj in queryset:
            Post.objects.filter(pk=obj.id)\
                .update(status=Post.APPROVED, timestamp=time.time())

        for obj in queryset:
            send_notif(user=obj.user, type=Notif.APPROVE, post=obj, actor=request.user)

    make_approve.short_description = u"تایید مطلب"

    def make_approve_go_default(modeladmin, request, queryset):
        queryset.update(status=1, show_in_default=True, timestamp=time.time())

    make_approve_go_default.short_description = u"تایید و ارسال برای صفحه اصلی"

    def no_problem(self, request, queryset):
        for obj in queryset:
            obj.report = 0
            obj.status = Post.APPROVED
            obj.save()

    no_problem.short_description = "عکس مشکلی نداره"

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 pin entry was"
        else:
            message_bit = "%s pin entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)

    really_delete_selected.short_description = "حذف انتخاب شده ها"

    def delete_all_user_posts(self, request, queryset):
        for obj in queryset:
            user = obj.user
            user.is_active = False
            user.save()
            Post.objects.filter(user=obj.user).delete()
            Comments.objects.filter(user=obj.user).delete()

    delete_all_user_posts.short_description = 'حذف تمام پست های کاربر و غیر فعال کردن'

    def fault(self, request, queryset):
        for obj in queryset:
            Post.objects.filter(pk=obj.id).update(status=Post.FAULT, report=0)
            #print obj.status
            #obj.status = Post.FAULT
            #print obj.status
            #obj.save()

            user = obj.user
            user.profile.fault = user.profile.fault+1
            user.profile.save()

        for obj in queryset:
            send_notif(user=obj.user, type=Notif.FAULT, post=obj, actor=request.user)

    fault.short_description = 'ثبت تخلف'


class NotifyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'seen', 'type')
    list_filter = ('seen',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'admin_image')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'website', 'cnt_post', 'cnt_like', 'score',
                    'user', 'trusted')
    search_fields = ['user__id', 'name']
    list_filter = ('trusted',)


class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'version', 'current')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'ip_address', 'is_public',
                    'reported', 'admin_link')

    list_filter = ('submit_date', 'is_public', 'reported')
    search_fields = ['ip_address', 'user__id']
    date_hierarchy = 'submit_date'

    actions = ['accept', 'unaccept', 'delete_and_deactive_user',
               'delete_all_user_comments']

    def accept(self, request, queryset):
        for obj in queryset:
            obj.is_public = True
            obj.save()
    accept.short_description = 'تایید'

    def unaccept(self, request, queryset):
        for obj in queryset:
            obj.is_public = False
            obj.save()
    unaccept.short_description = 'عدم تایید'

    def delete_and_deactive_user(self, request, queryset):
        for obj in queryset:
            user = obj.user
            user.is_active = False
            user.save()
            obj.delete()

    delete_and_deactive_user.short_description = 'حذف و غیر فعال کردن کاربر'

    def delete_all_user_comments(self, request, queryset):
        for obj in queryset:
            user = obj.user
            user.is_active = False
            user.save()
            Comments.objects.filter(user=obj.user).delete()

    delete_all_user_comments.short_description = 'حذف تمام کامنت های این کاربر و غیر فعال کردن کاربر'

admin.site.register(Post, PinAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(App_data, AppAdmin)
admin.site.register(Comments, CommentsAdmin)
