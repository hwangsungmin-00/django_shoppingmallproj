from django.contrib import admin
from .models import Post, Category, Manufacture, Comment
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.

admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Comment)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category, CategoryAdmin)

class ManufactureAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Manufacture, ManufactureAdmin)