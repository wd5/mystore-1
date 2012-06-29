# -*- coding: utf-8 -*-

import os
from django.db import models
from django.db.models.signals import pre_delete
from PIL import Image as PImage
import mptt
from utils.fields import ThumbnailImageField
import mystore.settings

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

class Attribute(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Атрибут')
    
    class Meta:
        db_table = 'attributes'
        verbose_name = 'Атрибут'
        verbose_name_plural = 'Атрибуты'
    
    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField('Название категории', max_length=50, unique=True)
    slug = models.SlugField('ЧПУ', max_length=50, unique=True,
        help_text=r'Уникальное значение для ЧПУ.')
    is_active = models.BooleanField('Включено', default=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    attributes = models.ManyToManyField(Attribute, verbose_name=u'Атрибуты', blank=True)
    parent = models.ForeignKey('self', blank=True, null=True,
        verbose_name="Родитель", related_name='child')
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return('catalog_category', (), { 'category_slug': self.slug })
   
class Product(models.Model):
    name = models.CharField('Название', max_length=255, unique=True)
    is_active = models.BooleanField('Включено', default=True)
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2)
    slug = models.SlugField('ЧПУ', max_length=255, unique=True,
        help_text='Уникальное значение для ЧПУ.')
    brand_url = models.CharField('Ссылка', max_length=255,
        help_text='Ссылка на сайт производителя.', blank=True)
    image = ThumbnailImageField(upload_to='images/products', verbose_name='Изображение')
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(Category, verbose_name='Категория')
    attributes = models.ManyToManyField(Attribute, through='ProductAttributeValue', verbose_name=u'Атрибуты', blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        
    def __unicode__(self):
        return self.name
   
    @models.permalink
    def get_absolute_url(self):
        """
        Get absolute url for our links in templates.
        """
        return ('catalog_product', (), { 'product_slug': self.slug })
    
    def get_attributes_values(self):
        """
        Get product attributes with their values.
        """
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute('SELECT attr.name, pav.value \
                        FROM product_attribute_value as pav \
                        INNER JOIN attributes as attr \
                            ON pav.attribute_id = attr.id \
                        WHERE pav.product_id = %s ;', [self.pk])
        return dictfetchall(cursor)
    
class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, verbose_name='Продукт')
    attribute = models.ForeignKey(Attribute, verbose_name='Атрибут')
    value = models.CharField('Значение', max_length='255')
    
    class Meta:
        db_table = 'product_attribute_value'
        ordering = ['attribute__name']
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
        
def pre_delete_handler(sender, **kwargs):
    """
    Delete main image and thumbnail after model is deleted.
    """
    #image_path = mystore.settings.MEDIA_ROOT + '/images/products'
    #main_path = os.path.join(image_path, kwargs['instance'].image.path)
    #thumb_path = os.path.join(mystore.settings.MEDIA_ROOT, kwargs['instance'].thumbnail)
    if os.path.exists(kwargs['instance'].image.path):
        os.remove(kwargs['instance'].image.path)
    if os.path.exists(kwargs['instance'].image.thumb_path):
        os.remove(kwargs['instance'].image.thumb_path)
    
pre_delete.connect(pre_delete_handler, sender=Product)
mptt.register(Category,)
