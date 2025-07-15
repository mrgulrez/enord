from django.contrib import admin

# Register your models here.
from .models import Categories, Products, ProductQuestions, ProductReviews
admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(ProductQuestions)
admin.site.register(ProductReviews)