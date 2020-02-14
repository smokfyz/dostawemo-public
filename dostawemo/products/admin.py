from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Product, Category, Color, Size, ProductImage
from nested_admin import NestedTabularInline, NestedModelAdmin


class ProductImageInline(NestedTabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(NestedModelAdmin, MarkdownxModelAdmin):
    inlines = [ ProductImageInline, ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)