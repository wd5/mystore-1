# -*- coding: utf-8 -*-

from django.contrib import admin
from feincms.admin import editor
from catalog.models import Product, Category, Attribute, ProductAttributeValue
from catalog.forms import ProductAdminForm
from utils import datastructures

class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1

def admin_image(obj):
    """
    Show product image in the admin interface.
    """
    return '<img style="max-width:200px;max-height:200px;" src="%s" />' % obj.image.url
admin_image.allow_tags = True
admin_image.short_description = 'Изображение'

class ProductAdmin(admin.ModelAdmin):
    fields = (('name', 'is_active'), 'price', 'slug', 'brand_url', 'image', 'description', 'category', ('meta_keywords', 'meta_description'))
    form = ProductAdminForm
    date_hierarchy = 'created_at'
    list_display = ('name', admin_image, 'price', 'category', 'created_at', 'updated_at', 'is_active')
    list_display_links = ('name',)
    list_editable = ('price', 'category')
    list_filter = ('is_active', 'category')
    list_per_page = 50
    ordering = ['-created_at']
    search_fields = ['name', 'price', 'brand_url', 'description', 'category__name' , 'meta_keywords', 'meta_description']
    prepopulated_fields = {'slug' : ('name',)}
    add_form_template = 'admin/add_form.html'
    inlines = (ProductAttributeValueInline,)
   
    def save_model(self, request, obj, form, change):
        """
        Saving product's category-based attributes with values
        """
        obj.save()
        attrv = request.POST.getlist('attrv[]')
        attrn = request.POST.getlist('attrn[]')
        for x in range(len(attrv)):
            if attrv[x] != '':
                pav = ProductAttributeValue()
                pav.attribute = Attribute.objects.get(pk=attrn[x])
                pav.product = obj
                pav.value = attrv[x]
                pav.save(force_insert=True)

class AttributeAdmin(admin.ModelAdmin):
    list_filter = ('category__name',)

class CategoryAdmin(editor.TreeEditor):
    fields = (('name', 'is_active'), 'slug', 'parent', 'attributes', ('meta_keywords', 'meta_description'))
    list_display = ('name', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ['name', 'parent__name' , 'meta_keywords', 'meta_description']
    prepopulated_fields = {'slug' : ('name',)}
    filter_horizontal = ('attributes',)
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Attribute, AttributeAdmin)
