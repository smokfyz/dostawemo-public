from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Purchase
from dostawemo.products.models import Product
from dostawemo.products.admin import ProductImageInline
from nested_admin import NestedStackedInline, NestedModelAdmin


class PurchaseProductInline(NestedStackedInline):
    model = Product
    extra = 0
    show_change_link = True
    classes = ('collapse', )
    inlines = [ ProductImageInline, ]


class PurchaseAdmin(NestedModelAdmin, MarkdownxModelAdmin):
    readonly_fields=('collected_amount',)
    inlines = [ PurchaseProductInline, ]


admin.site.register(Purchase, PurchaseAdmin)