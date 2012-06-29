# -*- coding: utf-8 -*-

from catalog.models import Category
from mystore import settings

def mystore(request):
    """
    Declare our own context processor.
    """
    return {
        'home_url': settings.SITE_URL,
        'active_categories': Category.objects.filter(is_active=True),
        'site_name': settings.SITE_NAME,
        'meta_keywords': settings.META_KEYWORDS,
        'meta_description': settings.META_DESCRIPTION,
        'request': request
    }
