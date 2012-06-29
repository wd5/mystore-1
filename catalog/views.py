# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core import serializers
from catalog.models import Category, Product, Attribute
from django.http import HttpResponse
import logging

def ajax_category(request):
    """
    Send attributes of product category in json format.
    Used in add_view product of admin-interface when user change product category.
    """
    if request.is_ajax():
        json_result = serializers.serialize("json", 
            Attribute.objects.filter(category__pk=request.GET['id']))
        return HttpResponse(json_result, mimetype="application/javascript")
    pass

def index(request, template_name="catalog/index.html"):
    """
    Index page with welcome-message.
    """
    page_title = 'My test store'
    return render_to_response(template_name, locals(),
        context_instance=RequestContext(request))
    
def show_category(request, category_slug, template_name="catalog/category.html"):
    """
    Show products in category by list.
    """
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render_to_response(template_name, locals(),
        context_instance=RequestContext(request))

def show_product(request, product_slug, template_name="catalog/product.html"):
    """
    Show product detail-page.
    """
    p = get_object_or_404(Product, slug=product_slug)
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    return render_to_response(template_name, locals(),
        context_instance=RequestContext(request))
