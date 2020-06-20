from django.contrib import admin

# Register your models here.
from . models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class PostAdmin(admin.ModelAdmin):
    list_display = ('id','content','posted_by')
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'commented_by')

class ReactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'reaction', 'reacted_by')
    
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reaction, ReactionAdmin)
admin.site.register(Group,GroupAdmin)