# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from catalog.models import Product

def search(request, template_name="catalog/search.html"):
    """
    Search products by containing query in name.
    """
    query = request.GET['q']
    products = Product.objects.filter(name__icontains=query).filter(is_active=True)
    return render_to_response(template_name, locals(),
        context_instance=RequestContext(request))
