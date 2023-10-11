
from django.contrib import admin
from blog.models import Postcode, BlogCommentcode

admin.site.register((BlogCommentcode))

@admin.register(Postcode)

class PostAdmin(admin.ModelAdmin):
    class Media:
        js= ('tinyInject.js',)